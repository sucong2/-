import React, { useState } from 'react';
import { Button, Grid, Typography } from '@material-ui/core';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/upload`, formData, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'student_report.pdf');
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error('Error uploading the file', error);
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
      </Grid>
      <Grid item xs={12}>
        <Button variant="contained" color="primary" onClick={handleUpload}>
          Upload and Generate Report
        </Button>
      </Grid>
      {file && (
        <Grid item xs={12}>
          <Typography variant="body1">{file.name}</Typography>
        </Grid>
      )}
    </Grid>
  );
}

export default FileUpload;