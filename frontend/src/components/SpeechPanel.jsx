import React, { useState, useEffect, useRef } from 'react';
import {
  Button,
  Box,
  Paper,
  Typography,
  Alert,
  IconButton,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import axios from 'axios';
import WaveSurfer from 'wavesurfer.js';

const API_URL = process.env.REACT_APP_API_URL;

const TextBox = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginTop: theme.spacing(1),
  marginBottom: theme.spacing(2),
  minHeight: '50px',
  borderRadius: theme.shape.borderRadius,
  border: `1px solid ${theme.palette.divider}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
}));

const TextBoxContainer = styled(Box)({
  position: 'relative',
  width: '100%',
});

const PlayButton = styled(IconButton)(({ theme }) => ({
  position: 'absolute',
  bottom: 8,
  right: 8,
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
  '&.MuiIconButton-root': {
    padding: 8,
  },
}));

const PulsingDot = styled('span')({
  width: '8px',
  height: '8px',
  borderRadius: '50%',
  display: 'inline-block',
  margin: '0 4px',
  animation: 'pulse 1.5s infinite',
  '@keyframes pulse': {
    '0%': { transform: 'scale(0.8)', opacity: 0.5 },
    '50%': { transform: 'scale(1.2)', opacity: 1 },
    '100%': { transform: 'scale(0.8)', opacity: 0.5 }
  }
});

const SpinningCircle = styled('span')({
  width: '16px',
  height: '16px',
  borderRadius: '50%',
  border: '2px solid currentColor',
  borderTopColor: 'transparent',
  display: 'inline-block',
  marginLeft: '8px',
  animation: 'spin 1s linear infinite',
  '@keyframes spin': {
    '0%': { transform: 'rotate(0deg)' },
    '100%': { transform: 'rotate(360deg)' }
  }
});

const SpeechPanel = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [status, setStatus] = useState('Ready to record...');
  const [recognition, setRecognition] = useState(null);
  const [currentLanguage, setCurrentLanguage] = useState('kn-IN');
  const [retrievedAudioUrl, setRetrievedAudioUrl] = useState('');
  const [waveform, setWaveform] = useState(null);
  const waveformRef = useRef(null);
  const containerRef = useRef(null);
  const [isWaveformReady, setIsWaveformReady] = useState(false);
  const [texts, setTexts] = useState({
    kannada: '',
    english: '',
    aiResponse: '',
    kannadaResponse: ''
  });

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setStatus('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognitionInstance = new SpeechRecognition();
    
    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = true;
    recognitionInstance.lang = currentLanguage;

    recognitionInstance.onresult = async (event) => {
      let interimTranscript = '';
      let finalTranscript = '';
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      const isKannada = currentLanguage === 'kn-IN';
      
      if (event.results[event.results.length - 1].isFinal) {
        try {
          setIsProcessing(true);
          setStatus('Processing...');

          let kannadaText = '';
          let englishText = '';

          if (isKannada) {
            kannadaText = finalTranscript;
            const englishResponse = await axios.post(`${API_URL}/translate`, {
              text: finalTranscript,
              from_lang: 'kn',
              to_lang: 'en'
            });
            englishText = englishResponse.data.translatedText;
          } else {
            englishText = finalTranscript;
            const kannadaResponse = await axios.post(`${API_URL}/translate`, {
              text: finalTranscript,
              from_lang: 'en',
              to_lang: 'kn'
            });
            kannadaText = kannadaResponse.data.translatedText;
          }

          setTexts(prev => ({
            ...prev,
            kannada: kannadaText,
            english: englishText
          }));

          const aiResponse = await axios.post(`${API_URL}/generate`, {
            question: englishText
          });

          const kannadaAIResponse = await axios.post(`${API_URL}/translate`, {
            text: aiResponse.data.response,
            from_lang: 'en',
            to_lang: 'kn'
          });

          const retrieveResponse = await axios.post(`${API_URL}/retrieve`, {
            text: kannadaText
          });

        //   console.log('Retrieve Response:', retrieveResponse.data.best_match_path);

          if (retrieveResponse.data.best_match_path) {
            // Construct full URL to audio file
            const audioUrl = `${API_URL}/audio/${retrieveResponse.data.best_match_path.split('\\').pop()}`;
            setRetrievedAudioUrl(audioUrl);
          }
        //   console.log('Retrieved Audio URL:', retrieveResponse.data.best_match_path);

          setTexts(prev => ({
            ...prev,
            aiResponse: aiResponse.data.response,
            kannadaResponse: kannadaAIResponse.data.translatedText
          }));

          setStatus('Done');
          setIsProcessing(false);

        } catch (error) {
          console.error('Error:', error);
          setStatus('Error processing speech');
          setIsProcessing(false);
        }
      }
    };

    recognitionInstance.onend = () => {
      if (isRecording) {
        recognitionInstance.start();
      }
    };

    setRecognition(recognitionInstance);

    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, [isRecording, currentLanguage]);

  useEffect(() => {
    if (retrievedAudioUrl && containerRef.current && !waveform) {
      const wavesurfer = WaveSurfer.create({
        container: containerRef.current,
        waveColor: '#4a9eff',
        progressColor: '#1976d2',
        height: 80,
        responsive: true,
        cursorWidth: 1,
        cursorColor: '#1976d2',
        barWidth: 2,
        barRadius: 3,
        barGap: 3,
      });
  
      wavesurfer.on('error', err => {
        console.error('WaveSurfer error:', err);
      });
  
      wavesurfer.load(retrievedAudioUrl);
      
      wavesurfer.on('ready', () => {
        // console.log('WaveSurfer is ready to play');
        setIsWaveformReady(true);
        });
  
      setWaveform(wavesurfer);
  
      return () => wavesurfer.destroy();
    }
  }, [retrievedAudioUrl]);
  

  const startRecording = () => {
    setIsRecording(true);
    setStatus('Recording...');
    recognition.start();
  };

  const stopRecording = () => {
    setIsRecording(false);
    setStatus('Processing...');
    recognition.stop();
  };

  const playText = (text, language) => {
    if (isPlaying) {
      window.speechSynthesis.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language;
    utterance.onstart = () => setIsPlaying(true);
    utterance.onend = () => {
      setIsPlaying(false);
      setStatus('Ready to record...');
    };
    window.speechSynthesis.speak(utterance);
  };

  return (
    <Box sx={{ mb: { xs: 8, sm: 10 } }}>
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', sm: 'row' },
        justifyContent: 'center', 
        gap: 2, 
        mb: 3 
      }}>
        <Button
          variant="contained"
          onClick={() => setCurrentLanguage(currentLanguage === 'kn-IN' ? 'en-US' : 'kn-IN')}
          sx={{ 
            minWidth: { xs: '100%', sm: '200px' },
            py: { xs: 1.5, sm: 2 }
          }}
        >
          {currentLanguage === 'kn-IN' ? 'Switch to English' : 'Switch to Kannada'}
        </Button>
        <Button
          variant="contained"
          startIcon={<MicIcon />}
          onClick={startRecording}
          disabled={isRecording}
          sx={{ 
            minWidth: { xs: '100%', sm: '200px' },
            py: { xs: 1.5, sm: 2 }
          }}
        >
          Start Recording
        </Button>
        <Button
          variant="contained"
          color="secondary"
          startIcon={<StopIcon />}
          onClick={stopRecording}
          disabled={!isRecording}
          sx={{ 
            minWidth: { xs: '100%', sm: '200px' },
            py: { xs: 1.5, sm: 2 }
          }}
        >
          Stop Recording
        </Button>
      </Box>

      <Alert
        severity={
          status.includes('Error') ? 'error'
          : status === 'Done' ? 'success'
          : status === 'Recording...' ? 'warning'
          : 'info'
        }
        sx={{
          mb: 3,
          opacity: isProcessing ? 0.8 : 1,
          transition: 'all 0.5s ease-in-out',
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}
      >
        <Box component="span" sx={{ flexGrow: 1 }}>
          {status}
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          {status === 'Recording...' && (
            <>
              <PulsingDot sx={{ backgroundColor: 'warning.main' }} />
              <PulsingDot sx={{ backgroundColor: 'warning.main', animationDelay: '0.2s' }} />
              <PulsingDot sx={{ backgroundColor: 'warning.main', animationDelay: '0.4s' }} />
            </>
          )}
          {status === 'Processing...' && <SpinningCircle />}
          {status === 'Ready to record...' && (
            <PulsingDot sx={{ backgroundColor: 'success.main' }} />
          )}
        </Box>
      </Alert>

      <Box sx={{ 
        display: 'grid', 
        gap: 3,
        gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }
      }}>
        {[
          { title: 'Recognized Speech (Kannada)', content: texts.kannada, lang: 'kn-IN' },
          { title: 'Recognized Speech (English)', content: texts.english, lang: 'en-US' },
          { title: 'AI Response (English)', content: texts.aiResponse, lang: 'en-US' },
          { title: 'AI Response (Kannada)', content: texts.kannadaResponse, lang: 'kn-IN' }
        ].map((item, index) => (
          <Box key={index}>
            <Typography variant="h6" sx={{ mb: 1, fontSize: { xs: '1rem', sm: '1.25rem' } }}>
              {item.title}
            </Typography>
            <TextBoxContainer>
              <TextBox elevation={1} sx={{
                p: { xs: 2, sm: 3 },
                minHeight: { xs: '80px', sm: '100px' },
                fontSize: { xs: '0.9rem', sm: '1rem' }
              }}>
                {item.content}
              </TextBox>
              {item.content && (
                <PlayButton
                  onClick={() => playText(item.content, item.lang)}
                  disabled={isPlaying}
                  size="small"
                >
                  <PlayArrowIcon fontSize="small" />
                </PlayButton>
              )}
            </TextBoxContainer>
          </Box>
        ))}
      </Box>

      <Box sx={{ 
        mt: 3, 
        p: 3, 
        bgcolor: 'background.paper', 
        borderRadius: 2,
        boxShadow: 1
        }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
            Retrieved Similar Audio
        </Typography>
        <Box ref={containerRef} sx={{ mb: 2 }} />
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
            <Button 
                variant="contained"
                onClick={() => waveform && waveform.isReady && waveform.playPause()}
                startIcon={<PlayArrowIcon />}
                disabled={!waveform || !waveform.isReady}
            >
                Play/Pause
            </Button>
            <Button 
                variant="outlined"
                onClick={() => waveform && waveform.isReady && waveform.stop()}
                startIcon={<StopIcon />}
                disabled={!waveform || !waveform.isReady}
            >
                Stop
            </Button>
        </Box>

        </Box>

    </Box>
  );
};

export default SpeechPanel;
