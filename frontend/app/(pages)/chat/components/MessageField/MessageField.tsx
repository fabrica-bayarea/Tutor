import { useState, forwardRef, useImperativeHandle } from "react";
import styles from "./MessageField.module.css";

type Message = {
  sender: "user" | "llm";
  content: string;
};

export type MessageFieldRef = {
  addMessage: (sender: "user" | "llm", content: string) => void;
  updateLastMessage: (newContent: string) => void;
  getAllMessages: () => Message[];
  deleteAllMessages: () => void;
};

const MessageField = forwardRef<MessageFieldRef>((props, ref) => {
  const [messages, setMessages] = useState<Message[]>([]);

  const addMessage = (sender: "user" | "llm", content: string) => {
    setMessages((prev) => [...prev, { sender, content }]);
  };

  const updateLastMessage = (newContent: string) => {
    setMessages((prev) => {
      if (prev.length === 0) return prev;
      const updated = [...prev];
      updated[updated.length - 1] = {
        ...updated[updated.length - 1],
        content: newContent,
      };
      return updated;
    });
  };

  const getAllMessages = () => {
    return messages;
  };

  const deleteAllMessages = () =>{
    setMessages([]);
  }

  useImperativeHandle(ref, () => ({
    addMessage,
    updateLastMessage,
    getAllMessages,
    deleteAllMessages,
  }));

  return (
    <section className={styles.MessageConteiner}>
      <section className={styles.MessageField}>
        {messages.map((msg, index) => (
          <article
            key={index}
            className={msg.sender === "user" ? styles.MessageUser : styles.MessageLLM}
          >
            <p>{msg.content}</p>
          </article>
        ))}
      </section>
    </section>
  );
});

export default MessageField;
