import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Grid, Typography, Button } from "@material-ui/core";
import CreateRoomPage from "./CreateRoomPage";
import MusicPlayer from "./MusicPlayer";

const Room = (props) => {
  const [guestCanPause, setGuestCanPause] = useState(false);
  const [votesToSkip, setVotesToSkip] = useState(2);
  const [isHost, setIsHost] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false);
  const [song, setSong] = useState({});
  const { roomCode } = useParams();
  const navigate = useNavigate();

  const getRoomDetails = () => {
    fetch("/api/get-room/" + "?code=" + roomCode)
      .then((response) => {
        if (!response.ok) {
          props.leaveRoomCallback();
          navigate("/");
        }
        return response.json();
      })
      .then((data) => {
        setVotesToSkip(data.votes_to_skip);
        setGuestCanPause(data.guest_can_pause);
        setIsHost(data.is_host);
        if (data.is_host) {
          authenticateSpotify();
        }
      })
      .catch((error) => {
        console.error("Error fetching room details:", error);
      });
  };

  useEffect(() => {
    getRoomDetails();
  }, []);

  useEffect(() => {
    const interval = setInterval(getCurrentSong, 1000);
    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  const authenticateSpotify = () => {
    fetch("/spotify/is-authenticated/")
      .then((response) => response.json())
      .then((data) => {
        setSpotifyAuthenticated(data.status);
        if (!data.status) {
          fetch("/spotify/get-auth-url/")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            })
            .catch((error) => console.error("Error fetching auth URL:", error));
        }
      })
      .catch((error) => console.error("Error checking authentication:", error));
  };

  const getCurrentSong = () => {
    fetch("/spotify/current-song")
      .then((response) => {
        if (!response.ok) {
          return {};
        }
        return response.json();
      })
      .then((data) => {
        setSong(data);
      })
      .catch((error) => console.error("Error fetching current song:", error));
  };

  const leaveButtonPressed = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/api/leave-room/", requestOptions).then((_response) => {
      props.leaveRoomCallback();
      navigate("/");
    });
  };

  const updateShowSettings = (value) => {
    setShowSettings(value);
  };

  const renderSettingsPage = () => {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <CreateRoomPage
            update={true}
            votesToSkip={votesToSkip}
            guestCanPause={guestCanPause}
            roomCode={roomCode}
            updateCallback={getRoomDetails} // Pass getRoomDetails as the callback
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={() => updateShowSettings(false)}
          >
            Close
          </Button>
        </Grid>
      </Grid>
    );
  };

  const renderSettingsButton = () => {
    return (
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          onClick={() => updateShowSettings(true)}
        >
          Settings
        </Button>
      </Grid>
    );
  };

  return (
    <>
      {showSettings ? (
        renderSettingsPage()
      ) : (
        <Grid container spacing={1}>
          <Grid item xs={12} align="center">
            <Typography variant="h6" component="h6">
              Code: {roomCode}
            </Typography>
          </Grid>
          <MusicPlayer {...song} />
          {isHost ? renderSettingsButton() : null}

          <Grid item xs={12} align="center">
            <Button
              variant="contained"
              color="secondary"
              onClick={leaveButtonPressed}
            >
              Leave Room
            </Button>
          </Grid>
        </Grid>
      )}
    </>
  );
};

export default Room;
