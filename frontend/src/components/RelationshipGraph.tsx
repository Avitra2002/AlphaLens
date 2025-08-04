import React, { useEffect, useRef, useState } from 'react';

interface Relationship {
  entity1: string;
  entity2: string;
  relationship_type: string;
  confidence: number;
  context: string;
}

interface GraphData {
  relationships: Relationship[];
  summary?: string;
}

interface Node {
  id: string;
  name: string;
  x: number;
  y: number;
  type: string;
}

interface Link {
  source: string;
  target: string;
  relationship: string;
  confidence: number;
  context: string;
  id: string;
}

interface Tooltip {
  visible: boolean;
  x: number;
  y: number;
  content: string;
}

interface RelationshipGraphProps {
  data: GraphData;
}

const RelationshipGraph: React.FC<RelationshipGraphProps> = ({ data }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [tooltip, setTooltip] = useState<Tooltip>({ visible: false, x: 0, y: 0, content: '' });

  useEffect(() => {
    if (!data?.relationships) return;

    const svg = svgRef.current;
    const container = containerRef.current;
    if (!svg || !container) return;
    
    const width = svg.clientWidth || 800;
    const height = svg.clientHeight || 600;

    // Clear previous content
    svg.innerHTML = '';

    // Create nodes from relationships
    const nodeMap = new Map<string, Node>();
    const links: Link[] = [];

    data.relationships.forEach((rel, index) => {
      // Add entity1 node
      if (!nodeMap.has(rel.entity1)) {
        nodeMap.set(rel.entity1, {
          id: rel.entity1,
          name: rel.entity1,
          x: Math.random() * (width - 100) + 50,
          y: Math.random() * (height - 100) + 50,
          type: 'entity'
        });
      }

      // Add entity2 node (if not empty)
      if (rel.entity2 && !nodeMap.has(rel.entity2)) {
        nodeMap.set(rel.entity2, {
          id: rel.entity2,
          name: rel.entity2,
          x: Math.random() * (width - 100) + 50,
          y: Math.random() * (height - 100) + 50,
          type: 'entity'
        });
      }

      // Add link
      if (rel.entity2) {
        links.push({
          source: rel.entity1,
          target: rel.entity2,
          relationship: rel.relationship_type,
          confidence: rel.confidence,
          context: rel.context,
          id: `link-${index}`
        });
      }
    });

    const nodes = Array.from(nodeMap.values());

    // Simple force simulation without D3
    const simulation = () => {
      // Center force
      const centerX = width / 2;
      const centerY = height / 2;
      
      nodes.forEach(node => {
        const dx = centerX - node.x;
        const dy = centerY - node.y;
        node.x += dx * 0.01;
        node.y += dy * 0.01;
      });

      // Repulsion between nodes
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[j].x - nodes[i].x;
          const dy = nodes[j].y - nodes[i].y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < 100) {
            const force = (100 - distance) / distance * 0.5;
            const fx = dx * force;
            const fy = dy * force;
            
            nodes[i].x -= fx;
            nodes[i].y -= fy;
            nodes[j].x += fx;
            nodes[j].y += fy;
          }
        }
      }

      // Link attraction
      links.forEach(link => {
        const source = nodes.find(n => n.id === link.source);
        const target = nodes.find(n => n.id === link.target);
        
        if (source && target) {
          const dx = target.x - source.x;
          const dy = target.y - source.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          const targetDistance = 150;
          
          if (distance > 0) {
            const force = (distance - targetDistance) / distance * 0.1;
            const fx = dx * force;
            const fy = dy * force;
            
            source.x += fx;
            source.y += fy;
            target.x -= fx;
            target.y -= fy;
          }
        }
      });

      // Keep nodes within bounds
      nodes.forEach(node => {
        node.x = Math.max(30, Math.min(width - 30, node.x));
        node.y = Math.max(30, Math.min(height - 30, node.y));
      });
    };

    // Run simulation
    const animate = () => {
      simulation();
      render();
      requestAnimationFrame(animate);
    };

    const getRelativeMousePosition = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      };
    };

    const render = () => {
      svg.innerHTML = '';

      // Create defs for arrowheads
      const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
      const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
      marker.setAttribute('id', 'arrowhead');
      marker.setAttribute('markerWidth', '10');
      marker.setAttribute('markerHeight', '7');
      marker.setAttribute('refX', '9');
      marker.setAttribute('refY', '3.5');
      marker.setAttribute('orient', 'auto');
      
      const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      polygon.setAttribute('points', '0 0, 10 3.5, 0 7');
      polygon.setAttribute('fill', '#666');
      
      marker.appendChild(polygon);
      defs.appendChild(marker);
      svg.appendChild(defs);

      // Draw links
      links.forEach(link => {
        const source = nodes.find(n => n.id === link.source);
        const target = nodes.find(n => n.id === link.target);
        
        if (source && target) {
          // Create a group for the link elements
          const linkGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
          
          // Visible line
          const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          line.setAttribute('x1', source.x.toString());
          line.setAttribute('y1', source.y.toString());
          line.setAttribute('x2', target.x.toString());
          line.setAttribute('y2', target.y.toString());
          line.setAttribute('stroke', '#666');
          line.setAttribute('stroke-width', '2');
          line.setAttribute('marker-end', 'url(#arrowhead)');
          
          // Invisible thicker line for easier hovering
          const hoverLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          hoverLine.setAttribute('x1', source.x.toString());
          hoverLine.setAttribute('y1', source.y.toString());
          hoverLine.setAttribute('x2', target.x.toString());
          hoverLine.setAttribute('y2', target.y.toString());
          hoverLine.setAttribute('stroke', 'transparent');
          hoverLine.setAttribute('stroke-width', '12'); // Much thicker for easier hovering
          hoverLine.style.cursor = 'pointer';
          
          hoverLine.addEventListener('mouseenter', (e: MouseEvent) => {
            const pos = getRelativeMousePosition(e);
            setTooltip({
              visible: true,
              x: pos.x,
              y: pos.y,
              content: `${link.relationship} (${(link.confidence * 100).toFixed(0)}%): ${link.context}`
            });
            // Highlight the visible line
            line.setAttribute('stroke', '#3b82f6');
            line.setAttribute('stroke-width', '3');
          });
          
          hoverLine.addEventListener('mouseleave', () => {
            setTooltip({ visible: false, x: 0, y: 0, content: '' });
            // Reset line style
            line.setAttribute('stroke', '#666');
            line.setAttribute('stroke-width', '2');
          });
          
          linkGroup.appendChild(line);
          linkGroup.appendChild(hoverLine);
          svg.appendChild(linkGroup);

          // Add relationship label
          const midX = (source.x + target.x) / 2;
          const midY = (source.y + target.y) / 2;
          
          const labelBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', midX.toString());
          text.setAttribute('y', (midY + 4).toString());
          text.setAttribute('text-anchor', 'middle');
          text.setAttribute('font-size', '11');
          text.setAttribute('fill', '#374151');
          text.setAttribute('font-weight', '600');
          text.textContent = link.relationship;
          
          // Get text dimensions for background
          svg.appendChild(text);
          const bbox = text.getBBox();
          
          labelBg.setAttribute('x', (bbox.x - 4).toString());
          labelBg.setAttribute('y', (bbox.y - 2).toString());
          labelBg.setAttribute('width', (bbox.width + 8).toString());
          labelBg.setAttribute('height', (bbox.height + 4).toString());
          labelBg.setAttribute('fill', 'white');
          labelBg.setAttribute('fill-opacity', '0.9');
          labelBg.setAttribute('rx', '4');
          labelBg.setAttribute('stroke', '#e5e7eb');
          labelBg.setAttribute('stroke-width', '1');
          
          svg.removeChild(text);
          svg.appendChild(labelBg);
          svg.appendChild(text);
        }
      });

      // Draw nodes
      nodes.forEach(node => {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', node.x.toString());
        circle.setAttribute('cy', node.y.toString());
        circle.setAttribute('r', '25');
        circle.setAttribute('fill', '#3b82f6');
        circle.setAttribute('stroke', '#1e40af');
        circle.setAttribute('stroke-width', '2');
        circle.style.cursor = 'pointer';
        
        circle.addEventListener('mouseenter', (e: MouseEvent) => {
          const pos = getRelativeMousePosition(e);
          setTooltip({
            visible: true,
            x: pos.x,
            y: pos.y,
            content: `Entity: ${node.name}`
          });
          // Highlight on hover
          circle.setAttribute('fill', '#2563eb');
          circle.setAttribute('r', '28');
        });
        
        circle.addEventListener('mouseleave', () => {
          setTooltip({ visible: false, x: 0, y: 0, content: '' });
          // Reset style
          circle.setAttribute('fill', '#3b82f6');
          circle.setAttribute('r', '25');
        });
        
        svg.appendChild(circle);

        // Add node label
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', node.x.toString());
        text.setAttribute('y', (node.y + 5).toString());
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-size', '12');
        text.setAttribute('font-weight', 'bold');
        text.setAttribute('fill', 'white');
        text.textContent = node.name.length > 8 ? node.name.substring(0, 8) + '...' : node.name;
        
        svg.appendChild(text);
      });
    };

    animate();
  }, [data]);

  return (
    <div ref={containerRef} className="relative w-full h-96 border rounded-lg bg-gray-50">
      <svg
        ref={svgRef}
        className="w-full h-full"
        style={{ minHeight: '400px' }}
      />
      
      {tooltip.visible && (
        <div
          className="absolute z-10 p-2 bg-gray-900 text-white text-sm rounded-lg shadow-lg pointer-events-none max-w-xs"
          style={{
            left: Math.min(tooltip.x + 10, containerRef.current?.clientWidth ? containerRef.current.clientWidth - 200 : tooltip.x + 10),
            top: tooltip.y - 40,
            transform: tooltip.x > (containerRef.current?.clientWidth || 0) / 2 ? 'translateX(-100%)' : 'none'
          }}
        >
          <div className="text-xs leading-relaxed">
            {tooltip.content}
          </div>
        </div>
      )}
      
      <div className="absolute top-2 left-2 bg-white px-3 py-1 rounded-lg shadow-sm text-sm font-medium">
        <strong>Relationship Graph</strong>
      </div>
    </div>
  );
};

export default RelationshipGraph;