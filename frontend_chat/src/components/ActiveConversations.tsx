import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ConversationModel } from '../models/Conversation';
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import ListGroup from 'react-bootstrap/ListGroup';
// @ts-ignore
import { NotificationContext } from '../contexts/NotificationContext.tsx';

export default function ActiveConversations() {
  const [conversations, setActiveConversations] = useState<ConversationModel[]>(
    []
  );
  const id = JSON.parse(document.getElementById('id')!.textContent!);
  // @ts-ignore
  const { unreadMessageCount } = useContext(NotificationContext);
  // @ts-ignore
  const { eachUser } = useContext(NotificationContext);

  useEffect(() => {
    async function fetchConversations() {
      fetch('/api/conversations/')
        .then((res) => res.json())
        .then(
          (result) => {
            setActiveConversations(result);
          },
          (error) => {
            console.log(error);
          }
        );
    }
    fetchConversations();
  });

  function createConversationName(user_id: string) {
    const sorted = [id, user_id].sort();
    return `conv${sorted[0]}_${sorted[1]}`;
  }

  function formatMessageTimestamp(
    timestamp: string | undefined
  ): [string, string] {
    if (!timestamp) return ['', ''];
    const date = new Date(timestamp);
    return [date.toLocaleTimeString().slice(0, 5), date.toLocaleDateString()];
  }

  function getNotifications(user_id: string) {
    let pickUser = eachUser.find((x: any) => x[0] == user_id);
    if (pickUser != undefined) {
      return pickUser[1];
    }
  }

  return (
    <div>
      <Card>
        <Card.Header
          style={{
            fontSize: '18px',
            background: '#499ef5',
            color: '#f8fbfe',
          }}
          className="px-4"
        >
          Conversations
          {unreadMessageCount > 0 && (
            <Badge
              pill
              bg="warning"
              style={{ height: 'fit-content' }}
              text="dark"
              className="mx-2"
            >
              {unreadMessageCount}
            </Badge>
          )}
        </Card.Header>
        <ListGroup variant="flush">
          {conversations.length > 0 ? (
            conversations
              .filter((conv) =>
                conv.name.slice(4).split('_').includes(String(id))
              )
              .sort((a: any, b: any) => {
                let aTimestamp = new Date(a.last_message.timestamp).getTime();
                let bTimestamp = new Date(b.last_message.timestamp).getTime();
                return bTimestamp - aTimestamp;
              })
              .map((c) => (
                <ListGroup.Item
                  action
                  className="py-0"
                  key={createConversationName(c.other_user.id)}
                >
                  <Link
                    to={`/chat/${createConversationName(
                      c.other_user.id
                    )}?conversation=${createConversationName(c.other_user.id)}`}
                  >
                    <div className="px-3">
                      <div
                        className="d-flex"
                        style={{
                          flexDirection: 'row',
                          justifyContent: 'space-between',
                        }}
                      >
                        <Card.Title>
                          {c.other_user.first_name} {c.other_user.last_name}
                          <Badge
                            pill
                            bg="primary"
                            style={{ height: 'fit-content' }}
                            className="mx-2"
                          >
                            {getNotifications(c.other_user.id)}
                          </Badge>
                        </Card.Title>

                        <p className="text-muted align-self-end mb-0">
                          {formatMessageTimestamp(
                            c.last_message?.timestamp
                          )[0] + ' '}
                          <span className="sender text-muted">
                            {
                              formatMessageTimestamp(
                                c.last_message?.timestamp
                              )[1]
                            }
                          </span>
                        </p>
                      </div>
                      <p className="text-muted">
                        {' '}
                        <span className="sender text-muted">
                          {c.last_message?.from_user.id === id ? 'you:  ' : ''}
                        </span>
                        {c.last_message?.text}
                      </p>
                    </div>
                  </Link>
                </ListGroup.Item>
              ))
          ) : (
            <div className="text-center text-muted my-5 py-5">
              No active conversations yet, to contact somebody start a chat from
              the post that interests you.
            </div>
          )}
        </ListGroup>
      </Card>
    </div>
  );
}
