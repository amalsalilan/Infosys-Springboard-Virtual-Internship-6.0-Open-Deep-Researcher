import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Switch } from './ui/switch';
import { 
  Search, 
  Globe, 
  Database, 
  BarChart3, 
  FileText, 
  Share2, 
  Download,
  Settings,
  ExternalLink,
  Zap,
  BookOpen,
  TrendingUp
} from 'lucide-react';

interface Tool {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: React.ComponentType<{ className?: string }>;
  status: 'active' | 'inactive' | 'premium';
  usage: number;
  connected: boolean;
}

export function ToolsPanel() {
  const [searchQuery, setSearchQuery] = useState('');

  const tools: Tool[] = [
    // Search & Discovery
    {
      id: 'tavily-search',
      name: 'Tavily Search Tool',
      description: 'AI-powered search engine for real-time web information',
      category: 'search',
      icon: Search,
      status: 'active',
      usage: 120,
      connected: true,
    },
    {
      id: 'web-search',
      name: 'Web Search',
      description: 'Search the web for current information and news',
      category: 'search',
      icon: Globe,
      status: 'active',
      usage: 85,
      connected: true,
    },
    {
      id: 'academic-search',
      name: 'Academic Search',
      description: 'Search academic papers and scholarly research',
      category: 'search',
      icon: BookOpen,
      status: 'active',
      usage: 45,
      connected: true,
    },
    
    // Analysis & Productivity
    {
      id: 'data-visualization',
      name: 'Data Visualization',
      description: 'Create charts, graphs, and visual representations',
      category: 'analysis',
      icon: TrendingUp,
      status: 'active',
      usage: 58,
      connected: true,
    },
    {
      id: 'citation-manager',
      name: 'Citation Manager',
      description: 'Generate and manage citations in various formats',
      category: 'productivity',
      icon: FileText,
      status: 'active',
      usage: 78,
      connected: true,
    },
  ];

  const categories = [
    { id: 'search', name: 'Search & Discovery', icon: Search },
    { id: 'analysis', name: 'Analysis', icon: BarChart3 },
    { id: 'productivity', name: 'Productivity', icon: FileText },
  ];

  const filteredTools = tools.filter(tool =>
    tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    tool.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'inactive': return 'bg-gray-500';
      case 'premium': return 'bg-purple-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Active';
      case 'inactive': return 'Inactive';
      case 'premium': return 'Premium';
      default: return 'Unknown';
    }
  };

  const ToolCard = ({ tool }: { tool: Tool }) => {
    const Icon = tool.icon;
    
    return (
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <CardTitle className="text-base">{tool.name}</CardTitle>
                <CardDescription className="text-sm">
                  {tool.description}
                </CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${getStatusColor(tool.status)}`} />
              <Badge variant={tool.status === 'premium' ? 'default' : 'secondary'} className="text-xs">
                {getStatusText(tool.status)}
              </Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Usage */}
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span>Usage this month</span>
                <span>{tool.usage} requests</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(tool.usage, 100)}%` }}
                />
              </div>
            </div>

            {/* Connection Status */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-sm">Connected</span>
                <div className={`w-2 h-2 rounded-full ${tool.connected ? 'bg-green-500' : 'bg-red-500'}`} />
              </div>
              <Switch checked={tool.connected} disabled={tool.status === 'premium'} />
            </div>

            {/* Actions */}
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="flex-1">
                <Settings className="w-4 h-4 mr-2" />
                Configure
              </Button>
              <Button variant="outline" size="sm">
                <ExternalLink className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="flex-1 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1>Tools & Integrations</h1>
            <p className="text-muted-foreground">
              Manage your research tools and external integrations
            </p>
          </div>
          <Button>
            <Download className="w-4 h-4 mr-2" />
            Install Tool
          </Button>
        </div>

        {/* Search */}
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            placeholder="Search tools..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Tools by Category */}
      <Tabs defaultValue="all" className="space-y-6">
        <TabsList>
          <TabsTrigger value="all">All Tools</TabsTrigger>
          {categories.map((category) => {
            const Icon = category.icon;
            const categoryTools = filteredTools.filter(t => t.category === category.id);
            return (
              <TabsTrigger key={category.id} value={category.id}>
                <Icon className="w-4 h-4 mr-2" />
                {category.name} ({categoryTools.length})
              </TabsTrigger>
            );
          })}
        </TabsList>

        <TabsContent value="all">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} />
            ))}
          </div>
        </TabsContent>

        {categories.map((category) => (
          <TabsContent key={category.id} value={category.id}>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredTools
                .filter(t => t.category === category.id)
                .map((tool) => (
                  <ToolCard key={tool.id} tool={tool} />
                ))}
            </div>
          </TabsContent>
        ))}
      </Tabs>

      {/* Usage Statistics */}
      <div className="mt-12">
        <h2 className="mb-4">Usage Statistics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Total Requests</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl">1,486</div>
              <p className="text-sm text-muted-foreground">This month</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Active Tools</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl">{tools.filter(t => t.status === 'active').length}</div>
              <p className="text-sm text-muted-foreground">Connected and working</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Success Rate</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl">98.5%</div>
              <p className="text-sm text-muted-foreground">Successful requests</p>
            </CardContent>
          </Card>
        </div>
      </div>

      {filteredTools.length === 0 && (
        <div className="text-center py-12">
          <Search className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg mb-2">No tools found</h3>
          <p className="text-muted-foreground">
            Try adjusting your search query
          </p>
        </div>
      )}
    </div>
  );
}