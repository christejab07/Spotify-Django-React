import React, { useState, useEffect } from "react";
import { render } from "react-dom";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
  useParams,
} from "react-router-dom";
import Homepage from "./Homepage";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import "../../static/css/index.css";

const App = () => {
  const [roomCode, setRoomCode] = useState(null);

  // Using useEffect to mimic componentDidMount behavior
  useEffect(() => {
    fetch("/api/user-in-room")
      .then((response) => response.json())
      .then((data) => {
        setRoomCode(data.code);
      });
    // async function fetchRoomCode() {
    //   try {
    //     const response = await fetch("/api/user-in-room");
    //     const data = await response.json();
    //     setRoomCode(data.code);
    //   } catch (error) {
    //     console.error("Error fetching room code:", error);
    //   }
    // }

    // fetchRoomCode(); // Call the function to fetch the room code
  }, []); // Empty dependency array means this effect runs once on mount

  const clearRoomCode = () => {
    setRoomCode(null);
  };

  // const RoomWrapper = () => {
  //   const { roomCode } = useParams();
  //   return <Room roomCode={roomCode} leaveRoomCallback={clearRoomCode} />;
  // };

  return (
    <div className="center">
      <Router>
        <Routes>
          <Route
            exact
            path="/"
            element={
              roomCode ? <Navigate to={`/room/${roomCode}`} /> : <Homepage />
            }
          />
          <Route path="/join" element={<RoomJoinPage />} />
          <Route path="/create" element={<CreateRoomPage />} />
          <Route
            path="/room/:roomCode"
            element={<Room leaveRoomCallback={clearRoomCode} />}
          />
        </Routes>
        {/* <p>There is home</p> */}
      </Router>
    </div>
  );
};

const appDiv = document.getElementById("app");
render(<App />, appDiv);

export default App;
