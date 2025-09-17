import { useState } from 'react';
import { Agent } from '../../FIGMA_CODE/src/App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Separator } from './ui/separator';
import { X, Search, MessageCircle, Settings2 } from 'lucide-react';

interface AgentPanelProps {
  agents: Agent[];
  selectedAgent: Agent | null;
  onSelectAgent: (agent: Agent) => void;
  onStartChat: (agent: Agent) => void;
  onClose: () => void;
  onConfigure: (agent: Agent) => void;
}

export function AgentPanel({ 
  agents, 
  selectedAgent, 
  onSelectAgent, 
  onStartChat, 
  onClose, 
  onConfigure 
}: AgentPanelProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    {
      name: 'Research Agents',
      agents: agents.filter(a => ['planner', 'research', 'writer'].includes(a.type)),
    },
  ];

  const filteredCategories = categories.map(category => ({
    ...category,
    agents: category.agents.filter(agent =>
      agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.description.toLowerCase().includes(searchQuery.toLowerCase())
    ),
  })).filter(category => category.agents.length > 0);

  return (
    <div className="w-[350px] bg-card border-r border-border flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h2>Research Agents</h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
        
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            placeholder="Search agents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Agent Categories */}
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-6">
          {filteredCategories.map((category) => (
            <div key={category.name} className="space-y-3">
              <h3 className="text-sm text-muted-foreground">{category.name}</h3>
              <div className="space-y-3">
                {category.agents.map((agent) => (
                  <Card
                    key={agent.id}
                    className={`cursor-pointer transition-colors ${
                      selectedAgent?.id === agent.id 
                        ? 'border-primary bg-primary/5' 
                        : 'hover:bg-accent'
                    }`}
                    onClick={() => onSelectAgent(agent)}
                  >
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                          <div className="text-2xl">{agent.icon}</div>
                          <div>
                            <CardTitle className="text-base">{agent.name}</CardTitle>
                            <CardDescription className="text-sm">
                              {agent.description}
                            </CardDescription>
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <div className="space-y-3">
                        {/* Tools */}
                        <div>
                          <p className="text-xs text-muted-foreground mb-2">
                            {agent.tools.length} tools available
                          </p>
                          <div className="flex flex-wrap gap-1">
                            {agent.tools.slice(0, 3).map((tool) => (
                              <Badge
                                key={tool}
                                variant="secondary"
                                className="text-xs"
                              >
                                {tool}
                              </Badge>
                            ))}
                            {agent.tools.length > 3 && (
                              <Badge variant="outline" className="text-xs">
                                +{agent.tools.length - 3} more
                              </Badge>
                            )}
                          </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            className="flex-1"
                            onClick={(e) => {
                              e.stopPropagation();
                              onStartChat(agent);
                            }}
                          >
                            <MessageCircle className="w-4 h-4 mr-2" />
                            Chat
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              onConfigure(agent);
                            }}
                          >
                            <Settings2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
              {category !== filteredCategories[filteredCategories.length - 1] && (
                <Separator className="my-4" />
              )}
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}