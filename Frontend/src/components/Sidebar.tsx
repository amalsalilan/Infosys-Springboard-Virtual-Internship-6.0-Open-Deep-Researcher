import { ViewType } from '../../FIGMA_CODE/src/App';
import { Button } from './ui/button';
import { 
  Home, 
  FolderOpen, 
  Bot, 
  Wrench, 
  Database, 
  Settings, 
  History,
  Brain
} from 'lucide-react';

interface SidebarProps {
  currentView: ViewType;
  onViewChange: (view: ViewType) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export function Sidebar({ currentView, onViewChange, collapsed, onToggleCollapse }: SidebarProps) {
  const navigationItems = [
    {
      id: 'welcome' as ViewType,
      label: 'Dashboard',
      icon: Home,
    },
    {
      id: 'projects' as ViewType,
      label: 'Research Projects',
      icon: FolderOpen,
    },
    {
      id: 'chat' as ViewType,
      label: 'Agents',
      icon: Bot,
    },
    {
      id: 'tools' as ViewType,
      label: 'Tools',
      icon: Wrench,
    },
    {
      id: 'knowledge' as ViewType,
      label: 'Knowledge Base',
      icon: Database,
    },
    {
      id: 'settings' as ViewType,
      label: 'Settings',
      icon: Settings,
    },
  ];

  return (
    <div className={`${collapsed ? 'w-[80px]' : 'w-[280px]'} bg-sidebar border-r border-sidebar-border flex flex-col transition-all duration-300`}>
      {/* Logo/Brand Area */}
      <div className="p-6 border-b border-sidebar-border">
        <div 
          className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
          onClick={onToggleCollapse}
        >
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary/80 rounded-lg flex items-center justify-center flex-shrink-0">
            <Brain className="w-6 h-6 text-primary-foreground" />
          </div>
          {!collapsed && (
            <div className="overflow-hidden">
              <h2 className="text-sidebar-foreground whitespace-nowrap">ResearchAI</h2>
              <p className="text-sm text-sidebar-foreground/60 whitespace-nowrap">Research Assistant</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 p-4">
        <div className="space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;
            
            return (
              <Button
                key={item.id}
                variant={isActive ? "secondary" : "ghost"}
                className={`w-full ${collapsed ? 'justify-center px-2' : 'justify-start gap-3'} h-11 ${
                  isActive 
                    ? 'bg-sidebar-accent text-sidebar-accent-foreground' 
                    : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                }`}
                onClick={() => onViewChange(item.id)}
                title={collapsed ? item.label : undefined}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {!collapsed && (
                  <span className="overflow-hidden whitespace-nowrap">{item.label}</span>
                )}
              </Button>
            );
          })}
        </div>
      </nav>

      {/* History Section */}
      <div className="p-4 border-t border-sidebar-border">
        <Button
          variant="ghost"
          className={`w-full ${collapsed ? 'justify-center px-2' : 'justify-start gap-3'} h-11 text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground`}
          title={collapsed ? 'History' : undefined}
        >
          <History className="w-5 h-5 flex-shrink-0" />
          {!collapsed && (
            <span className="overflow-hidden whitespace-nowrap">History</span>
          )}
        </Button>
      </div>

      {/* Footer */}
      {!collapsed && (
        <div className="p-4 border-t border-sidebar-border">
          <div className="text-xs text-sidebar-foreground/60">
            Version 1.0.0
          </div>
        </div>
      )}
    </div>
  );
}