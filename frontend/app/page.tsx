"use client";

import { useState } from "react";

export default function Home() {

    const [file, setFile] = useState<File | null>(null);

    const [query, setQuery] = useState("");

    const [messages, setMessages] = useState<any[]>([]);

    const [loading, setLoading] = useState(false);

    const [fileName, setFileName] = useState("");


    // ==============================
    // Upload PDF
    // ==============================

    const uploadPDF = async () => {

        if (!file) return;

        const formData = new FormData();

        formData.append("file", file);

        setLoading(true);

        try {

            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/upload-pdf`,
                {
                    method: "POST",
                    body: formData,
                }
            );

            const data = await response.json();

            setFileName(data.file_name);

            alert("PDF uploaded successfully");

        } catch (error) {

            console.error(error);

            alert("Upload failed");

        }

        setLoading(false);
    };


    // ==============================
    // Send Message
    // ==============================

    const sendMessage = async () => {

        if (!query) return;

        const userMessage = {
            role: "user",
            content: query,
        };

        setMessages((prev) => [...prev, userMessage]);

        setQuery("");

        setLoading(true);

        // Empty assistant message
        let assistantMessage = {
            role: "assistant",
            content: "",
        };

        setMessages((prev) => [...prev, assistantMessage]);

        try {

            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                    },

                    body: JSON.stringify({
                        session_id: "user1",
                        file_name: fileName,
                        query: userMessage.content,
                    }),
                }
            );

            const reader = response.body?.getReader();

            const decoder = new TextDecoder();

            let done = false;

            let streamedText = "";

            while (!done) {

                const result = await reader?.read();

                done = result?.done || false;

                const chunk = decoder.decode(result?.value || new Uint8Array());

                streamedText += chunk;

                assistantMessage.content = streamedText;

                setMessages((prev) => {

                    const updated = [...prev];

                    updated[updated.length - 1] = {
                        ...assistantMessage,
                    };

                    return updated;
                });
            }

        } catch (error) {

            console.error(error);

        }

        setLoading(false);
    };


    return (

        <main className="min-h-screen bg-black text-white flex flex-col items-center p-10">

            <h1 className="text-4xl font-bold mb-10">
                Resume RAG Chatbot
            </h1>


            {/* Upload Section */}

            <div className="w-full max-w-3xl bg-zinc-900 p-6 rounded-2xl mb-6">

                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => {

                        if (e.target.files?.[0]) {

                            setFile(e.target.files[0]);
                        }
                    }}
                />

                <button
                    onClick={uploadPDF}
                    className="bg-blue-600 px-4 py-2 rounded-lg ml-4"
                >
                    Upload PDF
                </button>

            </div>


            {/* Chat Section */}

            <div className="w-full max-w-3xl bg-zinc-900 rounded-2xl p-6 h-[600px] overflow-y-auto">

                <div className="space-y-4">

                    {messages.map((msg, index) => (

                        <div
                            key={index}
                            className={`p-4 rounded-xl max-w-[80%]
              ${msg.role === "user"
                                    ? "bg-blue-600 ml-auto"
                                    : "bg-zinc-700"
                                }`}
                        >

                            {msg.content}

                        </div>
                    ))}

                    {loading && (
                        <div className="text-zinc-400">
                            Thinking...
                        </div>
                    )}

                </div>

            </div>


            {/* Input */}

            <div className="w-full max-w-3xl flex gap-4 mt-6">

                <input
                    type="text"
                    placeholder="Ask question about resume..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="flex-1 p-4 rounded-xl bg-zinc-800 text-white outline-none"
                />

                <button
                    onClick={sendMessage}
                    className="bg-green-600 px-6 rounded-xl"
                >
                    Send
                </button>

            </div>

        </main>
    );
}