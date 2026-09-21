import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';

const remarkPlugins = [remarkGfm];
const rehypePlugins: React.ComponentProps<typeof ReactMarkdown>['rehypePlugins'] = [
  [rehypeHighlight, { detect: false, ignoreMissing: true }],
];

export function Markdown({ children }: { children: string }) {
  return (
    <div className="md">
      <ReactMarkdown remarkPlugins={remarkPlugins} rehypePlugins={rehypePlugins}>
        {children}
      </ReactMarkdown>
    </div>
  );
}
