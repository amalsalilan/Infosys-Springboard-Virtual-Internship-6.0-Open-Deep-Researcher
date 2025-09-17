import { useState } from 'react';
import { Sidebar } from "./components/Sidebar";
import { WelcomeScreen } from "./components/WelcomeScreen";
import { AgentPanel } from "./components/AgentPanel";
import { ChatInterface } from "./components/ChatInterface";
import { SettingsPanel } from "./components/SettingsPanel";
import { ProjectsPanel } from "./components/ProjectsPanel";
import { ToolsPanel } from "./components/ToolsPanel";
import { KnowledgeBasePanel } from "./components/KnowledgeBasePanel";
import {Button} from "./components/ui/button";
import { LogIn } from "lucide-react";



export type ViewType = 'welcome' | 'chat' | 'projects' | 'tools' | 'knowledge' | 'settings';
export type AgentType = 'planner' | 'research' | 'writer';

export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  description: string;
  tools: string[];
  icon: string;
  model?: string;
  temperature?: number;
  maxTokens?: number;
  systemPrompt?: string;
}

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  agentId?: string;
  sources?: Array<{
    title: string;
    url: string;
    snippet: string;
  }>;
  toolCalls?: Array<{
    tool: string;
    status: 'running' | 'completed' | 'error';
    result?: string;
  }>;
}

export interface Project {
  id: string;
  title: string;
  description: string;
  progress: number;
  lastModified: Date;
  collaborators: string[];
  tags: string[];
  status: 'active' | 'completed' | 'archived';
}

export default function App() {
  const [currentView, setCurrentView] = useState<ViewType>('welcome');
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [agentPanelOpen, setAgentPanelOpen] = useState(false);
  const [settingsPanelOpen, setSettingsPanelOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const agents: Agent[] = [
    {
      id: 'planner',
      name: 'The Planner Agent',
      type: 'planner',
      description: 'Strategic planning and project coordination for research tasks',
      tools: ['Task Planning', 'Project Management', 'Timeline Creation', 'Resource Allocation'],
      icon: '📋',
      model: 'GPT-4',
      temperature: 0.3,
      maxTokens: 6000,
    },
    {
      id: 'research',
      name: 'Research Agent',
      type: 'research',
      description: 'Comprehensive research across academic and web sources',
      tools: ['Tavily Search Tool', 'Academic Search', 'Web Search', 'Data Collection'],
      icon: '🔍',
      model: 'GPT-4',
      temperature: 0.4,
      maxTokens: 8000,
    },
    {
      id: 'writer',
      name: 'The Writer Agent',
      type: 'writer',
      description: 'Professional writing and content creation for research outputs',
      tools: ['Document Generation', 'Citation Manager', 'Content Editing', 'Report Writing'],
      icon: '✍️',
      model: 'GPT-4',
      temperature: 0.6,
      maxTokens: 8000,
    },
  ];

  const handleStartChat = (agent: Agent) => {
    setSelectedAgent(agent);
    setCurrentView('chat');
    setAgentPanelOpen(true);
    setMessages([]);
  };

  const handleSendMessage = (content: string) => {
    if (!selectedAgent) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
      agentId: selectedAgent.id,
    };

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      content: `I'm ${selectedAgent.name}. I'll help you with ${content.toLowerCase()}. Let me search for relevant information...`,
      role: 'assistant',
      timestamp: new Date(),
      agentId: selectedAgent.id,
      toolCalls: [
        {
          tool: selectedAgent.tools[0],
          status: 'running',
        },
      ],
    };

    setMessages(prev => [...prev, userMessage, assistantMessage]);
  };

  const handleLogin = () => {
    // Handle login logic here
    setIsLoggedIn(!isLoggedIn);
  };

  const renderMainContent = () => {
    switch (currentView) {
      case 'welcome':
        return (
          <WelcomeScreen 
            onStartResearch={() => {
              setCurrentView('chat');
              setAgentPanelOpen(true);
            }}
            onQuickAction={(type: string) => {
              // Default to research agent for quick actions
              const agent = agents.find(a => a.type === 'research') || agents[0];
              handleStartChat(agent);
            }}
          />
        );
      case 'chat':
        return (
          <div className="flex flex-1 min-h-0">
            {agentPanelOpen && (
              <AgentPanel
                agents={agents}
                selectedAgent={selectedAgent}
                onSelectAgent={setSelectedAgent}
                onStartChat={handleStartChat}
                onClose={() => setAgentPanelOpen(false)}
                onConfigure={(agent) => {
                  setSelectedAgent(agent);
                  setSettingsPanelOpen(true);
                }}
              />
            )}
            <ChatInterface
              selectedAgent={selectedAgent}
              messages={messages}
              onSendMessage={handleSendMessage}
              onToggleAgentPanel={() => setAgentPanelOpen(!agentPanelOpen)}
            />
            {settingsPanelOpen && (
              <SettingsPanel
                agent={selectedAgent}
                onClose={() => setSettingsPanelOpen(false)}
                onSave={(updatedAgent) => {
                  setSelectedAgent(updatedAgent);
                  setSettingsPanelOpen(false);
                }}
              />
            )}
          </div>
        );
      case 'projects':
        return <ProjectsPanel projects={projects} />;
      case 'tools':
        return <ToolsPanel />;
      case 'knowledge':
        return <KnowledgeBasePanel />;
      case 'settings':
        return (
          <div className="flex-1 p-6">
            <h1>Settings</h1>
            <p>Application settings and preferences</p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex h-screen bg-background">
      <Sidebar
        currentView={currentView}
        onViewChange={setCurrentView}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      <main className="flex-1 min-w-0 flex flex-col">
        {/* Top Header with Login Button */}
        <header className="flex justify-end items-center p-4 border-b border-border bg-card">
          <Button 
            variant={isLoggedIn ? "outline" : "default"}
            size="sm"
            onClick={handleLogin}
            className="flex items-center gap-2"
          >
            <LogIn className="w-4 h-4" />
            {isLoggedIn ? "Sign Out" : "Log In"}
          </Button>
        </header>
        
        {/* Main Content */}
        <div className="flex-1 min-h-0">
          {renderMainContent()}
        </div>
      </main>
    </div>
  );
}