import React from "react";
import {
  Grid,
  Typography,
  Card,
  IconButton,
  LinearProgress,
} from "@material-ui/core";
import { PlayArrow, SkipNext, Pause } from "@material-ui/icons";
const MusicPlayer = (props) => {
  const songProgress = (props.progress / props.duration) * 100;

  const skipSong = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/spotify/skip", requestOptions)
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };
  const pauseSong = () => {
    const requestOptions = {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
    };

    fetch("/spotify/pause", requestOptions)
      .then((response) => {
        if (response.ok) {
          console.log("Song paused successfully");
        } else {
          console.error("Failed to pause song");
        }
      })
      .catch((error) =>
        console.error("An error occurred while pausing the song", error)
      );
  };

  const playSong = () => {
    const requestOptions = {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
    };

    fetch("/spotify/play", requestOptions)
      .then((response) => {
        if (response.ok) {
          console.log("Song played successfully");
        } else {
          console.error("Failed to play song");
        }
      })
      .catch((error) =>
        console.error("An error occurred while playing the song", error)
      );
  };

  return (
    <Card>
      <Grid container alignItems="center">
        <Grid item xs={4} align="center">
          <img src={props.image_url} height="100%" width="100%" />
        </Grid>
        <Grid item xs={8} align="center">
          <Typography component="h5" variant="h5">
            {props.title}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            {props.artist}
          </Typography>
          <div>
            <IconButton onClick={props.is_playing ? pauseSong : playSong}>
              {props.is_playing ? <Pause /> : <PlayArrow />}
            </IconButton>
            <IconButton onClick={skipSong}>
              {props.votes} / {props.votes_required}
              <SkipNext />
            </IconButton>
          </div>
        </Grid>
      </Grid>
      <LinearProgress variant="determinate" value={songProgress} />
    </Card>
  );
};

export default MusicPlayer;
