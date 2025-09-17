import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Upload, 
  Search, 
  FileText, 
  Link, 
  Filter,
  MoreHorizontal,
  CheckCircle,
  Clock,
  AlertCircle,
  Trash2,
  Download,
  Eye,
  Tag
} from 'lucide-react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from './ui/dropdown-menu';

interface Document {
  id: string;
  title: string;
  type: 'pdf' | 'url' | 'text' | 'docx';
  size?: string;
  status: 'processing' | 'completed' | 'error';
  uploadDate: Date;
  tags: string[];
  processingProgress?: number;
  chunks?: number;
}

export function KnowledgeBasePanel() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  // Mock documents for demonstration
  const documents: Document[] = [
    {
      id: '1',
      title: 'Climate Change and Coastal Ecosystems.pdf',
      type: 'pdf',
      size: '2.4 MB',
      status: 'completed',
      uploadDate: new Date('2024-01-15'),
      tags: ['Climate', 'Environment', 'Research'],
      chunks: 245,
    },
    {
      id: '2',
      title: 'Machine Learning Trends Report',
      type: 'url',
      status: 'completed',
      uploadDate: new Date('2024-01-14'),
      tags: ['ML', 'Technology', 'Trends'],
      chunks: 89,
    },
    {
      id: '3',
      title: 'Statistical Methods in Healthcare.docx',
      type: 'docx',
      size: '1.8 MB',
      status: 'processing',
      uploadDate: new Date('2024-01-16'),
      tags: ['Healthcare', 'Statistics'],
      processingProgress: 65,
    },
    {
      id: '4',
      title: 'Quantum Computing Overview',
      type: 'text',
      size: '0.5 MB',
      status: 'error',
      uploadDate: new Date('2024-01-13'),
      tags: ['Quantum', 'Physics', 'Computing'],
    },
  ];

  const allTags = Array.from(new Set(documents.flatMap(doc => doc.tags)));

  const filteredDocuments = documents.filter(doc => {
    const matchesSearch = doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         doc.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    
    const matchesCategory = selectedCategory === 'all' || 
                          (selectedCategory === 'completed' && doc.status === 'completed') ||
                          (selectedCategory === 'processing' && doc.status === 'processing') ||
                          (selectedCategory === 'error' && doc.status === 'error');
    
    const matchesTags = selectedTags.length === 0 || 
                       selectedTags.some(tag => doc.tags.includes(tag));
    
    return matchesSearch && matchesCategory && matchesTags;
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'processing': return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'error': return <AlertCircle className="w-4 h-4 text-red-500" />;
      default: return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'pdf': return '📄';
      case 'url': return '🔗';
      case 'text': return '📝';
      case 'docx': return '📋';
      default: return '📄';
    }
  };

  const DocumentCard = ({ document }: { document: Document }) => (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="text-2xl">{getTypeIcon(document.type)}</div>
            <div className="flex-1">
              <CardTitle className="text-base line-clamp-1">{document.title}</CardTitle>
              <CardDescription className="text-sm">
                {document.size && `${document.size} • `}
                {document.uploadDate.toLocaleDateString()}
                {document.chunks && ` • ${document.chunks} chunks`}
              </CardDescription>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIcon(document.status)}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm">
                  <MoreHorizontal className="w-4 h-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem>
                  <Eye className="w-4 h-4 mr-2" />
                  View
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Download className="w-4 h-4 mr-2" />
                  Download
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Tag className="w-4 h-4 mr-2" />
                  Edit Tags
                </DropdownMenuItem>
                <DropdownMenuItem className="text-destructive">
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {/* Processing Progress */}
          {document.status === 'processing' && document.processingProgress && (
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span>Processing</span>
                <span>{document.processingProgress}%</span>
              </div>
              <Progress value={document.processingProgress} className="h-2" />
            </div>
          )}

          {/* Tags */}
          <div className="flex flex-wrap gap-1">
            {document.tags.map((tag) => (
              <Badge key={tag} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>

          {/* Status */}
          <div className="text-sm text-muted-foreground">
            Status: {document.status.charAt(0).toUpperCase() + document.status.slice(1)}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="flex-1 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1>Knowledge Base</h1>
            <p className="text-muted-foreground">
              Manage documents and build your research knowledge base
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline">
              <Link className="w-4 h-4 mr-2" />
              Add URL
            </Button>
            <Button>
              <Upload className="w-4 h-4 mr-2" />
              Upload Files
            </Button>
          </div>
        </div>

        {/* Upload Area */}
        <Card className="border-2 border-dashed border-muted-foreground/25 hover:border-muted-foreground/50 transition-colors mb-6">
          <CardContent className="p-8">
            <div className="text-center">
              <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg mb-2">Upload Documents</h3>
              <p className="text-muted-foreground mb-4">
                Drag and drop files here, or click to browse
              </p>
              <div className="flex items-center justify-center gap-4 text-sm text-muted-foreground">
                <span>Supported: PDF, DOCX, TXT, URLs</span>
                <span>•</span>
                <span>Max: 100MB per file</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Search and Filters */}
        <div className="flex gap-4 mb-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search documents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9"
            />
          </div>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger className="w-[180px]">
              <Filter className="w-4 h-4 mr-2" />
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Documents</SelectItem>
              <SelectItem value="completed">Completed</SelectItem>
              <SelectItem value="processing">Processing</SelectItem>
              <SelectItem value="error">Error</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Tag Filters */}
        <div className="flex flex-wrap gap-2 mb-6">
          {allTags.map((tag) => (
            <Badge
              key={tag}
              variant={selectedTags.includes(tag) ? "default" : "outline"}
              className="cursor-pointer"
              onClick={() => {
                if (selectedTags.includes(tag)) {
                  setSelectedTags(selectedTags.filter(t => t !== tag));
                } else {
                  setSelectedTags([...selectedTags, tag]);
                }
              }}
            >
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      {/* Documents */}
      <Tabs defaultValue="grid" className="space-y-6">
        <TabsList>
          <TabsTrigger value="grid">Grid View</TabsTrigger>
          <TabsTrigger value="list">List View</TabsTrigger>
        </TabsList>

        <TabsContent value="grid">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredDocuments.map((document) => (
              <DocumentCard key={document.id} document={document} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="list">
          <div className="space-y-4">
            {filteredDocuments.map((document) => (
              <Card key={document.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 flex-1">
                      <div className="text-2xl">{getTypeIcon(document.type)}</div>
                      <div className="flex-1">
                        <h3 className="font-medium">{document.title}</h3>
                        <p className="text-sm text-muted-foreground">
                          {document.size && `${document.size} • `}
                          {document.uploadDate.toLocaleDateString()}
                          {document.chunks && ` • ${document.chunks} chunks`}
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {document.tags.slice(0, 3).map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                        {document.tags.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{document.tags.length - 3}
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {getStatusIcon(document.status)}
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="w-4 h-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem>
                            <Eye className="w-4 h-4 mr-2" />
                            View
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Download className="w-4 h-4 mr-2" />
                            Download
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Tag className="w-4 h-4 mr-2" />
                            Edit Tags
                          </DropdownMenuItem>
                          <DropdownMenuItem className="text-destructive">
                            <Trash2 className="w-4 h-4 mr-2" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Statistics */}
      <div className="mt-12">
        <h2 className="mb-4">Knowledge Base Statistics</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Total Documents</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl">{documents.length}</div>
              <p className="text-sm text-muted-foreground">Uploaded</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Processed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl">{documents.filter(d => d.status === 'completed').length}</div>
              <p className="text-sm text-muted-foreground">Ready for search</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Total Chunks</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl">
                {documents.reduce((sum, doc) => sum + (doc.chunks || 0), 0)}
              </div>
              <p className="text-sm text-muted-foreground">Searchable pieces</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Storage Used</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl">12.8 MB</div>
              <p className="text-sm text-muted-foreground">Of 1GB limit</p>
            </CardContent>
          </Card>
        </div>
      </div>

      {filteredDocuments.length === 0 && (
        <div className="text-center py-12">
          <FileText className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg mb-2">No documents found</h3>
          <p className="text-muted-foreground mb-4">
            {searchQuery || selectedTags.length > 0 
              ? 'Try adjusting your search or filters' 
              : 'Upload your first document to get started'
            }
          </p>
          <Button>
            <Upload className="w-4 h-4 mr-2" />
            Upload Files
          </Button>
        </div>
      )}
    </div>
  );
}