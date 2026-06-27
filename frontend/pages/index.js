import { useState, useRef, useEffect } from 'react';
import { uploadPDF, sendMessage, getChatHistory } from '../lib/api';
import { Send, Upload, MessageCircle, Loader } from 'lucide-react';

export default function Home() {
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [pdfLoaded, setPdfLoaded] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    try {
      const result = await uploadPDF(file, sessionId);
      if (result.message) {
        setPdfLoaded(true);
        setMessages([{ type: 'system', content: `✅ ${result.message}` }]);
      }
    } catch (error) {
      setMessages([{ type: 'error', content: 'Upload failed' }]);
    }
    setLoading(false);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { type: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const result = await sendMessage(input, sessionId);
      setMessages(prev => [...prev, { type: 'ai', content: result.answer, source: result.source }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'error', content: 'Error: Could not get response' }]);
    }
    setLoading(false);
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col">
        <div className="flex items-center gap-2 mb-8">
          <MessageCircle className="w-8 h-8 text-indigo-600" />
          <h1 className="text-xl font-bold text-gray-800">RAG Chat</h1>
        </div>

        {/* Upload Section */}
        <div className="mb-6">
          <label className="flex flex-col items-center justify-center w-full p-4 border-2 border-dashed border-indigo-300 rounded-lg cursor-pointer bg-indigo-50 hover:bg-indigo-100">
            <Upload className="w-6 h-6 text-indigo-600 mb-2" />
            <span className="text-sm font-medium text-gray-700">Upload PDF</span>
            <input type="file" accept=".pdf" onChange={handleUpload} className="hidden" />
          </label>
        </div>

        {pdfLoaded && <div className="text-sm text-green-600 font-medium">✅ PDF Ready</div>}
        
        <div className="mt-auto text-xs text-gray-500">
          <p>Session: {sessionId.slice(0, 10)}...</p>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                msg.type === 'user' ? 'bg-indigo-600 text-white' :
                msg.type === 'error' ? 'bg-red-100 text-red-800' :
                msg.type === 'system' ? 'bg-green-100 text-green-800' :
                'bg-gray-200 text-gray-800'
              }`}>
                <p className="text-sm">{msg.content}</p>
                {msg.source && <p className="text-xs mt-1 opacity-75">Source: {msg.source}</p>}
              </div>
            </div>
          ))}
          {loading && <div className="flex justify-start"><Loader className="w-5 h-5 animate-spin text-indigo-600" /></div>}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Box */}
        <div className="border-t border-gray-200 bg-white p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask a question..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              disabled={loading}
            />
            <button
              onClick={handleSend}
              disabled={loading}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
