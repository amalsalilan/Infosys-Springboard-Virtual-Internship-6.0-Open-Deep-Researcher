import { useState } from 'react';
import { Agent } from '../../FIGMA_CODE/src/App';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Slider } from './ui/slider';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Checkbox } from './ui/checkbox';
import { ScrollArea } from './ui/scroll-area';
import { X, Save } from 'lucide-react';

interface SettingsPanelProps {
  agent: Agent | null;
  onClose: () => void;
  onSave: (agent: Agent) => void;
}

export function SettingsPanel({ agent, onClose, onSave }: SettingsPanelProps) {
  const [localAgent, setLocalAgent] = useState<Agent | null>(agent);

  if (!localAgent) return null;

  const availableTools = [
    'Web Search',
    'Academic Database Search',
    'Document Analysis',
    'Data Visualization',
    'Code Execution',
    'Citation Generator',
    'Statistical Analysis',
    'PubMed',
    'arXiv',
    'GitHub Search',
    'Stack Overflow',
    'Market Data',
    'Competitor Analysis',
    'Trend Analysis',
    'Financial Data',
    'Python Code',
    'R Analysis',
  ];

  const models = [
    'GPT-4',
    'GPT-4 Turbo',
    'Claude 3 Opus',
    'Claude 3 Sonnet',
    'Claude 3 Haiku',
    'Gemini Pro',
  ];

  const handleSave = () => {
    onSave(localAgent);
  };

  const updateAgent = (updates: Partial<Agent>) => {
    setLocalAgent(prev => prev ? { ...prev, ...updates } : null);
  };

  return (
    <div className="w-[300px] bg-card border-l border-border flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between">
          <h2>Agent Configuration</h2>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-4 h-4" />
          </Button>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          Configure {localAgent.name}
        </p>
      </div>

      {/* Configuration Tabs */}
      <ScrollArea className="flex-1">
        <div className="p-4">
          <Tabs defaultValue="general" className="space-y-4">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="general">General</TabsTrigger>
              <TabsTrigger value="tools">Tools</TabsTrigger>
              <TabsTrigger value="rag">RAG</TabsTrigger>
            </TabsList>
            
            <TabsContent value="general" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Model Settings</CardTitle>
                  <CardDescription>Configure the AI model and parameters</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>Model</Label>
                    <Select 
                      value={localAgent.model} 
                      onValueChange={(value) => updateAgent({ model: value })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select model" />
                      </SelectTrigger>
                      <SelectContent>
                        {models.map((model) => (
                          <SelectItem key={model} value={model}>
                            {model}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label>Temperature</Label>
                      <span className="text-sm text-muted-foreground">
                        {localAgent.temperature}
                      </span>
                    </div>
                    <Slider
                      value={[localAgent.temperature || 0.7]}
                      onValueChange={([value]) => updateAgent({ temperature: value })}
                      max={1}
                      min={0}
                      step={0.1}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">
                      Lower values for more focused responses, higher for creativity
                    </p>
                  </div>

                  <div className="space-y-2">
                    <Label>Max Tokens</Label>
                    <Input
                      type="number"
                      value={localAgent.maxTokens}
                      onChange={(e) => updateAgent({ maxTokens: parseInt(e.target.value) })}
                      min={100}
                      max={32000}
                    />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base">System Prompt</CardTitle>
                  <CardDescription>Customize the agent's behavior and personality</CardDescription>
                </CardHeader>
                <CardContent>
                  <Textarea
                    value={localAgent.systemPrompt || ''}
                    onChange={(e) => updateAgent({ systemPrompt: e.target.value })}
                    placeholder="Enter custom system prompt..."
                    rows={4}
                  />
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="tools" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Available Tools</CardTitle>
                  <CardDescription>Select which tools this agent can use</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {availableTools.map((tool) => (
                      <div key={tool} className="flex items-center space-x-2">
                        <Checkbox
                          id={tool}
                          checked={localAgent.tools.includes(tool)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              updateAgent({ tools: [...localAgent.tools, tool] });
                            } else {
                              updateAgent({ 
                                tools: localAgent.tools.filter(t => t !== tool) 
                              });
                            }
                          }}
                        />
                        <Label htmlFor={tool} className="text-sm">
                          {tool}
                        </Label>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="rag" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Knowledge Base</CardTitle>
                  <CardDescription>Configure RAG and document access</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>Knowledge Base Selection</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select knowledge base" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="default">Default Knowledge Base</SelectItem>
                        <SelectItem value="academic">Academic Papers</SelectItem>
                        <SelectItem value="technical">Technical Documentation</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Embedding Model</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select embedding model" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="ada-002">text-embedding-ada-002</SelectItem>
                        <SelectItem value="3-small">text-embedding-3-small</SelectItem>
                        <SelectItem value="3-large">text-embedding-3-large</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Search Parameters</Label>
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <Label className="text-xs">Top K</Label>
                        <Input type="number" defaultValue="5" min="1" max="20" />
                      </div>
                      <div>
                        <Label className="text-xs">Similarity</Label>
                        <Input type="number" defaultValue="0.7" min="0" max="1" step="0.1" />
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </ScrollArea>

      {/* Save Button */}
      <div className="p-4 border-t border-border">
        <Button onClick={handleSave} className="w-full">
          <Save className="w-4 h-4 mr-2" />
          Save Configuration
        </Button>
      </div>
    </div>
  );
}