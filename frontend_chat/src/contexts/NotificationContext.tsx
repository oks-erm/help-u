import React, { createContext, ReactNode, useContext, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

const DefaultProps = {
  unreadMessageCount: 0,
  connectionStatus: "Uninstantiated"
};

export interface NotificationProps {
  unreadMessageCount: number;
  connectionStatus: string;
}

export const NotificationContext = createContext<NotificationProps>(DefaultProps);

export const NotificationContextProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [unreadMessageCount, setUnreadMessageCount] = useState(0);

  const { readyState } = useWebSocket( `wss://8000-okserm-helpu-4vq7cec76g9.ws-eu74.gitpod.io/notifications/`, {
    onOpen: () => {
      console.log("Connected to Notifications!");
    },
    onClose: () => {
      console.log("Disconnected from Notifications!");
    },
    onMessage: (e) => {
      const data = JSON.parse(e.data);
      switch (data.type) {
        default:
          console.error("Unknown message type!");
          break;
        case "unread_count":
          setUnreadMessageCount(data.unread_count);
          break;
        case "new_message_notification":
          setUnreadMessageCount((count) => (count += 1));
          break;
      }
    }
  });

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated"
  }[readyState];

  return (
    <NotificationContext.Provider value={{ unreadMessageCount, connectionStatus }}>
      {children}
    </NotificationContext.Provider>
  );
};