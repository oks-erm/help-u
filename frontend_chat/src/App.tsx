import React, {useState}  from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import Chat from "./components/Chat.tsx";
import ActiveConversations from "./components/ActiveConversations.tsx";
import { NotificationContextProvider } from "./contexts/NotificationContext.tsx";

export default function App() {
    return (
      <Router basename='/messages/'>
        <Routes>
          <Route path="" element={
            <NotificationContextProvider>
              <ActiveConversations />
            </NotificationContextProvider>} />
          <Route path="chat/:conversationName" element={<Chat />} />
        </Routes>
      </Router>
    );
  };
