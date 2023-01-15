import * as React from 'react';
import ReactDOM from 'react-dom';
import { useState, useEffect, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { Link, useParams } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InfiniteScroll from 'react-infinite-scroll-component';
// @ts-ignore
import { ChatLoader } from './ChatLoader.tsx';
import { MessageModel } from '../models/Message';
import { ConversationModel } from '../models/Conversation';
// @ts-ignore
import { Message } from './Message.tsx';
import ListGroup from 'react-bootstrap/ListGroup';
import Card from 'react-bootstrap/Card';
import { UserModel } from '../models/User';

export interface NotificationProps {
  unreadMessageCount: number;
  connectionStatus: string;
  eachUser: Array<Array<number>>;
}

export default function Chat() {
  const [messageHistory, setMessageHistory] = useState<any>([]);
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<ConversationModel | null>(
    null
  );
  const { conversationName } = useParams();
  const [to_user, setToUser] = useState<UserModel>();
  const [page, setPage] = useState(2);
  const [hasMoreMessages, setHasMoreMessages] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const scrollToBottom = () => {
    messagesEndRef?.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
    });
  };

  const { readyState, sendJsonMessage } = useWebSocket(
    `wss://helpukr.herokuapp.com/messages/chat/${conversationName}`,
    {
      onOpen: () => {
        console.log('Connected!');
      },
      onClose: () => {
        console.log('Disconnected!');
      },
      onMessage: (e) => {
        const data = JSON.parse(e.data);
        switch (data.type) {
          case 'chat_message_echo':
            setMessageHistory((prev: any) => [data.message, ...prev]);
            sendJsonMessage({
              type: 'read_messages',
            });
            break;
          case 'last_50_messages':
            setMessageHistory(data.messages);
            setHasMoreMessages(data.has_more);
            setToUser(data.to_user);
            break;
          default:
            console.error('Unknown message type!');
            break;
        }
      },
    }
  );

  // to make sure a conversation name is the same for both users
  function transformConversationName(conversationName?: string) {
    const split: any = conversationName
      ?.slice(4)
      .split('_')
      .sort((a: any, b: any) => {
        return a - b;
      });
    return `conv${split[0]}_${split[1]}`;
  }

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  useEffect(scrollToBottom, [messageHistory]);

  useEffect(() => {
    if (connectionStatus === 'Open') {
      sendJsonMessage({
        type: 'read_messages',
      });
    }
  }, [connectionStatus, sendJsonMessage]);

  async function fetchMessages() {
    const apiRes = await fetch(
      `https://helpukr.herokuapp.com/api/messages/?conversation=${transformConversationName(
        conversationName
      )}&page=${page}`,
      {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      }
    );
    if (apiRes.status === 200) {
      const data: {
        count: number;
        next: string | null;
        previous: string | null;
        results: MessageModel[];
      } = await apiRes.json();
      setHasMoreMessages(data.next !== null);
      setPage(page + 1);
      setMessageHistory((prev: MessageModel[]) => prev.concat(data.results));
    }
  }

  function handleChangeMessage(e: any) {
    setMessage(e.target.value);
  }

  const handleSubmit = () => {
    if (message.length === 0) return;
    if (message.length > 512) return;
    sendJsonMessage({
      type: 'chat_message',
      message,
    });
    setMessage('');
  };

  useEffect(() => {
    async function fetchConversation() {
      const apiRes = await fetch(
        `https://helpukr.herokuapp.com/api/conversations/${transformConversationName(
          conversationName
        )}/`,
        {
          method: 'GET',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
        }
      );
      if (apiRes.status === 200) {
        const data: ConversationModel = await apiRes.json();
        setConversation(data);
      }
    }
    fetchConversation();
  }, [transformConversationName(conversationName)]);

  return (
    <div className="ms-2 me-2">
      <Card
        style={{
          height: '75vh',
          display: 'flex',
          justifyContent: 'space-between',
          background: 'url(https://i.imgur.com/rogZEKl.jpeg)',
          backgroundRepeat: 'repeat-y',
        }}
      >
        <Card.Header
          style={{
            background: '#499ef5',
            color: '#f8fbfe',
          }}
          className="px-4"
        >
          <Link to={'/'}>
            <i
              className="bx bxs-chevron-left bx-flip-vertical px-2 pb-1"
              style={{
                fontSize: '21px',
                color: '#f8fbfe',
              }}
            ></i>
          </Link>
          {to_user?.first_name} {to_user?.last_name}
        </Card.Header>
        <div
          id="scrollableDiv"
          style={{
            overflow: 'auto',
            display: 'flex',
            flexDirection: 'column-reverse',
          }}
        >
          <InfiniteScroll
            dataLength={messageHistory.length}
            next={fetchMessages}
            className="d-flex"
            style={{
              flexDirection: 'column-reverse',
            }}
            inverse={true}
            hasMore={hasMoreMessages}
            loader={<ChatLoader />}
            scrollableTarget="scrollableDiv"
          >
            <div ref={messagesEndRef} />
            {messageHistory.map((message: MessageModel) => (
              <Message key={message.id} message={message} />
            ))}
          </InfiniteScroll>
        </div>
      </Card>

      <div className="d-flex">
        <Form.Control
          style={{
            display: 'inline-block',
          }}
          name="message"
          placeholder="Message"
          onChange={handleChangeMessage}
          value={message}
        />
        <Button
          style={{
            fontSize: '20px',
            border: '0',
            background: 'none',
            marginLeft: '-45px',
          }}
          onClick={handleSubmit}
        >
          <i
            className="bx bxs-send bx-flip-vertical"
            style={{ color: '#2680e0' }}
          ></i>
        </Button>
      </div>
    </div>
  );
}
