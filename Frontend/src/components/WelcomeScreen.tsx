import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Plus, Send } from 'lucide-react';

interface WelcomeScreenProps {
  onStartResearch: () => void;
  onQuickAction: (type: string) => void;
}

export function WelcomeScreen({ onStartResearch, onQuickAction }: WelcomeScreenProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onStartResearch();
    }
  };

  const handleFileUpload = () => {
    // Handle document upload
    console.log('Document upload clicked');
  };

  return (
    <div className="h-full w-full flex items-center justify-center p-8">
      <div className="w-full max-w-2xl">
        <form onSubmit={handleSubmit} className="relative">
          <div className="relative flex items-center">
            <Input
              type="text"
              placeholder="Start new research"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="pr-20 h-14 text-lg border-2 rounded-xl shadow-sm focus:shadow-md transition-shadow"
            />
            <div className="absolute right-2 flex items-center gap-1">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-10 w-10 p-0 hover:bg-accent"
                onClick={handleFileUpload}
              >
                <Plus className="w-5 h-5" />
              </Button>
              <Button
                type="submit"
                size="sm"
                className="h-10 w-10 p-0"
                disabled={!inputValue.trim()}
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}