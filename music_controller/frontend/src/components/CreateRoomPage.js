import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  Grid,
  Typography,
  Button,
  TextField,
  FormHelperText,
  FormControl,
  Radio,
  RadioGroup,
  FormControlLabel,
  Collapse,
} from "@material-ui/core";
import Alert from "@mui/material/Alert";

const CreateRoomPage = ({
  votesToSkip = 2,
  guestCanPause = true,
  update = false,
  roomCode = null,
  updateCallback = () => {},
}) => {
  const [guestCanPauseState, setGuestCanPauseState] = useState(guestCanPause);
  const [votesToSkipState, setVotesToSkipState] = useState(votesToSkip);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const navigate = useNavigate();

  const handleVotesChange = (e) => {
    setVotesToSkipState(e.target.value);
  };

  const handleGuestCanPauseChange = (e) => {
    setGuestCanPauseState(e.target.value === "true");
  };

  const handleRoomButtonPressed = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: votesToSkipState,
        guest_can_pause: guestCanPauseState,
      }),
    };
    fetch("/api/create-room/", requestOptions)
      .then((response) => response.json())
      .then((data) => navigate("/room/" + data.code))
      .catch((error) => console.error(error));
  };

  const handleUpdateButtonPressed = () => {
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: votesToSkipState,
        guest_can_pause: guestCanPauseState,
        code: roomCode,
      }),
    };
    fetch("/api/update-room/", requestOptions).then((response) => {
      if (response.ok) {
        setSuccessMsg("Room updated successfully!");
      } else {
        setErrorMsg("Error updating room...");
      }
      updateCallback();
    });
  };

  const renderCreateButtons = () => (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={handleRoomButtonPressed}
        >
          Create A Room
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  );

  const renderUpdateButtons = () => (
    <Grid item xs={12} align="center">
      <Button
        color="primary"
        variant="contained"
        onClick={handleUpdateButtonPressed}
      >
        Update Room
      </Button>
    </Grid>
  );

  const title = update ? "Update Room" : "Create a Room";

  return (
    <div>
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Collapse in={errorMsg !== "" || successMsg !== ""}>
            {successMsg ? (
              <Alert severity="success" onClose={() => setSuccessMsg("")}>
                {successMsg}
              </Alert>
            ) : (
              <Alert severity="error" onClose={() => setErrorMsg("")}>
                {errorMsg}
              </Alert>
            )}
          </Collapse>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            {title}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <span align="center">Guest Control of Playback State</span>
            </FormHelperText>
            <RadioGroup
              row
              value={guestCanPauseState.toString()}
              onChange={handleGuestCanPauseChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              required
              type="number"
              onChange={handleVotesChange}
              value={votesToSkipState}
              inputProps={{
                min: 1,
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText>
              <span align="center">Votes Required To Skip Song</span>
            </FormHelperText>
          </FormControl>
        </Grid>
        {update ? renderUpdateButtons() : renderCreateButtons()}
      </Grid>
    </div>
  );
};

export default CreateRoomPage;
