import React, {useState}  from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import Chat from "./components/Chat.tsx";
import ActiveConversations from "./components/ActiveConversations.tsx";


export default function App() {
    return (
      <Router basename='/messages/'>
        <Routes>
          <Route path="" element={<ActiveConversations />} />
          <Route path="chat/:conversationName" element={<Chat />} />
        </Routes>
      </Router>
    );
  };
