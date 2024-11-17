import { styled, createTheme } from '@mui/material/styles';
import { Box, Paper } from '@mui/material';

const WaveAnimation = styled('div')({
    height: '50px',
    background: 'linear-gradient(90deg, #BB86FC 0%, #03DAC6 100%)',
    borderRadius: '20px',
    animation: 'wave 1.5s infinite ease-in-out',
    '@keyframes wave': {
      '0%': { transform: 'scaleY(0.2)' },
      '50%': { transform: 'scaleY(1)' },
      '100%': { transform: 'scaleY(0.2)' }
    }
});

const FloatingCard = styled(Paper)(({ theme }) => ({
    transform: 'perspective(1000px) rotateX(5deg)',
    transition: 'all 0.3s ease',
    '&:hover': {
      transform: 'perspective(1000px) rotateX(0deg) translateY(-10px)',
      boxShadow: theme.shadows[15]
    }
}));

const GlassPanel = styled(Box)({
    background: 'rgba(255, 255, 255, 0.1)',
    backdropFilter: 'blur(10px)',
    borderRadius: '20px',
    border: '1px solid rgba(255, 255, 255, 0.2)'
});

const theme = createTheme({
    palette: {
      primary: {
        main: '#6C63FF',
        light: '#8B85FF',
        dark: '#4B45B3'
      },
      secondary: {
        main: '#FF6584',
        light: '#FF8DA3',
        dark: '#B3475C'
      }
    },
    typography: {
      h1: {
        fontSize: 'clamp(2rem, 8vw, 4rem)',
        fontWeight: 700,
        letterSpacing: '-0.02em'
      }
    }
});

const DynamicBackground = styled(Box)({
    background: 'radial-gradient(circle at top right, #BB86FC22 0%, transparent 70%)',
    animation: 'gradient 15s ease infinite',
    '@keyframes gradient': {
      '0%': { backgroundPosition: '0% 50%' },
      '50%': { backgroundPosition: '100% 50%' },
      '100%': { backgroundPosition: '0% 50%' }
    }
});

const LoadingDots = styled('div')({
    display: 'flex',
    gap: '8px',
    '& span': {
      width: '8px',
      height: '8px',
      borderRadius: '50%',
      animation: 'bounce 0.5s alternate infinite'
    }
});

// Add global styles for scrollbar in a separate style tag or CSS file
const GlobalStyles = {
  '::-webkit-scrollbar': {
    width: '8px'
  },
  '::-webkit-scrollbar-thumb': {
    background: 'linear-gradient(45deg, #BB86FC, #03DAC6)',
    borderRadius: '4px'
  }
};

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
  

export { 
    WaveAnimation, 
    FloatingCard, 
    GlassPanel, 
    theme,
    DynamicBackground,
    LoadingDots,
    GlobalStyles,
    PulsingDot,
    SpinningCircle
};
