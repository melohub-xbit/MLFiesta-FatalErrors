import React, { useState } from 'react';
import {
  ThemeProvider,
  CssBaseline,
  Container,
  Box,
  Typography,
  IconButton,
  Link
} from '@mui/material';
import { createTheme } from '@mui/material/styles';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import GitHubIcon from '@mui/icons-material/GitHub';
import { motion } from 'framer-motion';
import SpeechPanel from './components/SpeechPanel';

const App = () => {
  const [mode, setMode] = useState('dark');

  const theme = createTheme({
    palette: {
      mode,
      primary: {
        main: mode === 'dark' ? '#BB86FC' : '#1976d2',
      },
      secondary: {
        main: mode === 'dark' ? '#03DAC6' : '#dc004e',
      },
      background: {
        default: mode === 'dark' ? '#121212' : '#f5f5f5',
        paper: mode === 'dark' ? '#1E1E1E' : '#ffffff',
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Box sx={{ minHeight: '100vh', py: { xs: 2, sm: 4 } }}>
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Box sx={{ 
              display: 'flex', 
              flexDirection: { xs: 'column', sm: 'row' },
              justifyContent: 'space-between', 
              alignItems: 'center', 
              mb: { xs: 2, sm: 4 },
              gap: { xs: 2, sm: 0 }
            }}>
              <Typography
                variant="h3"
                component="h1"
                sx={{
                  fontSize: { xs: '1.8rem', sm: '2.5rem', md: '3rem' },
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(45deg, #BB86FC 30%, #03DAC6 90%)'
                    : 'linear-gradient(45deg, #1976d2 30%, #dc004e 90%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 'bold',
                  textAlign: { xs: 'center', sm: 'left' }
                }}
              >
                Kannada Speech Q&A
              </Typography>
              <IconButton
                onClick={() => setMode(mode === 'dark' ? 'light' : 'dark')}
                sx={{
                  p: { xs: 1, sm: 2 },
                  transition: 'transform 0.3s ease-in-out',
                  '&:hover': { transform: 'rotate(180deg)' }
                }}
              >
                {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
              </IconButton>
            </Box>
            <SpeechPanel />
          </motion.div>
        </Box>
      </Container>
      <Box
        component="footer"
        sx={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          right: 0,
          textAlign: 'center',
          py: { xs: 1, sm: 2 },
          px: { xs: 2, sm: 0 },
          backdropFilter: 'blur(10px)',
          background: theme.palette.mode === 'dark'
            ? 'rgba(0,0,0,0.3)'
            : 'rgba(255,255,255,0.3)',
          borderTop: `1px solid ${theme.palette.divider}`
        }}
      >
        <Typography variant="body2" sx={{ fontSize: { xs: '0.8rem', sm: '1rem' } }}>
          <Link
            href="https://github.com/melohub-xbit/MLFiesta-FatalErrors"
            target="_blank"
            rel="noopener noreferrer"
            sx={{
              color: theme.palette.text.primary,
              textDecoration: 'none',
              display: 'inline-flex',
              alignItems: 'center',
              gap: 0.5,
              '&:hover': {
                color: theme.palette.primary.main
              }
            }}
          >
            View on GitHub <GitHubIcon sx={{ fontSize: { xs: 14, sm: 16 } }} />
          </Link>
        </Typography>
      </Box>
    </ThemeProvider>
  );
};

export default App;
