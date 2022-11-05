import React, { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ConversationModel } from "../models/Conversation";
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';


export default function ActiveConversations() {
  const [conversations, setActiveConversations] = useState<ConversationModel[]>([]);
  const id = JSON.parse(document.getElementById('id').textContent);

  useEffect(() => {
    async function fetchConversations() {
        fetch("/api/conversations/")
        .then(res => res.json())
        .then(
          (result) => {
            setActiveConversations(result);
          },
          (error) => {
            console.log(error)
          })
        };
    fetchConversations();
  });

  function createConversationName(user_id: string) {
    const sorted = [id, user_id].sort();
    return `conv${sorted[0]}_${sorted[1]}`;
  }

  function formatMessageTimestamp(timestamp?: string) {
    if (!timestamp) return;
    const date = new Date(timestamp);
    return date.toLocaleTimeString().slice(0, 5);
  }

  return (
    <div>
      <Card>
      <Card.Header
      style={{
        fontSize: "18px",
        background: "#499ef5",
        color: "#f8fbfe"
    }}
      className="px-4">
          Chats
      </Card.Header>
      <ListGroup variant='flush'>
      {conversations.map((c) => (
          <ListGroup.Item action
          className="py-0">
        <Link
          to={`/chat/${createConversationName(c.other_user.id)}?conversation=${createConversationName(c.other_user.id)}`}
          key={createConversationName(c.other_user.id)}
        >
          <div className="px-3">
            <div
            className="d-flex"
            style={{
              flexDirection: 'row',
              justifyContent: 'space-between'
            }}
            >
            <Card.Title>{c.other_user.first_name} {c.other_user.last_name}</Card.Title>
            <p className="text-muted align-self-end mb-0">{formatMessageTimestamp(c.last_message?.timestamp)}</p>
            </div>
            <p className="text-muted">{c.last_message?.text}</p>
            </div>
        </Link>
      </ListGroup.Item>
      ))}
       </ListGroup>
      </Card>
    </div>
  );
}