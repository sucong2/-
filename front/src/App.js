import React from 'react';
import { Container, CssBaseline, Typography } from '@material-ui/core';
import FileUpload from './components/FileUpload';

function App() {
  return (
    <div>
      <CssBaseline />
      <Container maxWidth="md">
        <Typography variant="h4" component="h1" gutterBottom>
          Student Performance Dashboard
        </Typography>
        <FileUpload />
      </Container>
    </div>
  );
}

export default App;