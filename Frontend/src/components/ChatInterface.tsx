import { useState, useRef, useEffect } from 'react';
import { Agent, Message } from '../../FIGMA_CODE/src/App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { ScrollArea } from './ui/scroll-area';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { 
  Send, 
  Paperclip, 
  Mic, 
  Settings, 
  Bot, 
  User, 
  ExternalLink,
  Loader2,
  Eye,
  EyeOff,
  Menu
} from 'lucide-react';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from './ui/collapsible';

interface ChatInterfaceProps {
  selectedAgent: Agent | null;
  messages: Message[];
  onSendMessage: (message: string) => void;
  onToggleAgentPanel: () => void;
}

export function ChatInterface({ 
  selectedAgent, 
  messages, 
  onSendMessage,
  onToggleAgentPanel 
}: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState('');
  const [hideToolCalls, setHideToolCalls] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && selectedAgent) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  if (!selectedAgent) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
        <Bot className="w-16 h-16 text-muted-foreground mb-4" />
        <h3 className="text-xl mb-2">No Agent Selected</h3>
        <p className="text-muted-foreground mb-6 max-w-md">
          Choose an AI research agent from the panel to start your conversation.
        </p>
        <Button onClick={onToggleAgentPanel}>
          <Menu className="w-4 h-4 mr-2" />
          Select Agent
        </Button>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col">
      {/* Chat Header */}
      <div className="border-b border-border p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={onToggleAgentPanel}
            >
              <Menu className="w-4 h-4" />
            </Button>
            <div className="text-2xl">{selectedAgent.icon}</div>
            <div>
              <div className="flex items-center gap-2">
                <h2>{selectedAgent.name}</h2>
                <div className="w-2 h-2 bg-green-500 rounded-full" title="Online" />
              </div>
              <p className="text-sm text-muted-foreground">
                {selectedAgent.description}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setHideToolCalls(!hideToolCalls)}
            >
              {hideToolCalls ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </Button>
            <Button variant="ghost" size="sm">
              <Settings className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4 max-w-4xl mx-auto">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <div className="text-2xl">{selectedAgent.icon}</div>
              </div>
              <h3 className="text-lg mb-2">Start a conversation</h3>
              <p className="text-muted-foreground">
                I'm {selectedAgent.name}, ready to help with your research needs.
              </p>
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-4 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              
              <div
                className={`max-w-2xl space-y-2 ${
                  message.role === 'user' ? 'text-right' : 'text-left'
                }`}
              >
                <div
                  className={`inline-block p-4 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-primary text-primary-foreground ml-12'
                      : 'bg-card border'
                  }`}
                >
                  <p>{message.content}</p>
                </div>

                {/* Tool Calls */}
                {message.toolCalls && !hideToolCalls && (
                  <div className="space-y-2">
                    {message.toolCalls.map((toolCall, index) => (
                      <Card key={index} className="bg-muted/50">
                        <CardContent className="p-3">
                          <div className="flex items-center gap-2">
                            {toolCall.status === 'running' && (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            )}
                            <span className="text-sm">
                              🔍 {toolCall.tool}
                              {toolCall.status === 'running' && '...'}
                            </span>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}

                {/* Sources */}
                {message.sources && (
                  <div className="space-y-2">
                    <p className="text-xs text-muted-foreground">Sources:</p>
                    {message.sources.map((source, index) => (
                      <Collapsible key={index}>
                        <CollapsibleTrigger asChild>
                          <Card className="cursor-pointer hover:bg-accent transition-colors">
                            <CardContent className="p-3">
                              <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                  <ExternalLink className="w-4 h-4" />
                                  <span className="text-sm truncate">{source.title}</span>
                                </div>
                                <Badge variant="outline" className="text-xs">
                                  View
                                </Badge>
                              </div>
                            </CardContent>
                          </Card>
                        </CollapsibleTrigger>
                        <CollapsibleContent>
                          <Card>
                            <CardContent className="p-3 text-sm text-muted-foreground">
                              {source.snippet}
                            </CardContent>
                          </Card>
                        </CollapsibleContent>
                      </Collapsible>
                    ))}
                  </div>
                )}

                <div className="text-xs text-muted-foreground">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>

              {message.role === 'user' && (
                <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="border-t border-border p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex items-end gap-2">
            <div className="flex-1 relative">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={`Ask ${selectedAgent.name} anything...`}
                className="pr-20"
                disabled={!selectedAgent}
              />
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex items-center gap-1">
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="h-8 w-8 p-0"
                >
                  <Paperclip className="w-4 h-4" />
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="h-8 w-8 p-0"
                >
                  <Mic className="w-4 h-4" />
                </Button>
              </div>
            </div>
            <Button
              type="submit"
              disabled={!inputValue.trim() || !selectedAgent}
              className="h-10 px-4"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={hideToolCalls}
                  onChange={(e) => setHideToolCalls(e.target.checked)}
                  className="w-3 h-3"
                />
                Hide Tool Calls
              </label>
            </div>
            <div>
              Model: {selectedAgent.model} | Tokens: {selectedAgent.maxTokens}
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}