import React, { useContext, useEffect, useReducer, useState } from "react";
import { Link, useParams } from "react-router-dom";

interface UserResponse {
  first_name: string;
  last_name: string;
  id: string;
}

export default function Conversations() {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const id = JSON.parse(document.getElementById('id').textContent);
  const [user, setUser] = useState<UserResponse[]>([]);

  useEffect(() => {
    async function fetchUsers() {
      fetch('/api/users/all')
        .then(res => res.json())
        .then(
          (result) => {
            setUsers(result);
            setUser(result.find((u:any) => u.id === id));
          },
          (error) => {
            console.log(error)
          }
        )};
    fetchUsers()
  });

  function createConversationName(user_id: string) {
    const sorted = [id, user_id].sort();
    return `conv${sorted[0]}_${sorted[1]}`;
  }

  return (
    <div>
      <h1>{user.first_name} {user.last_name} Chats</h1>
      {users
        .filter((u) => u.id !== id)
        .map((u) => (
          <Link
            key={u.id}
            to={`chat/${createConversationName(u.id)}`}
          >
            <div>{u.first_name} {u.last_name}</div>
          </Link>
        ))}
    </div>
  );
}
