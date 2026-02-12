import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

# Colors
colors = {
    'client': '#E3F2FD',
    'frontend': '#BBDEFB',
    'backend': '#90CAF9',
    'database': '#64B5F6',
    'text': '#1565C0',
    'arrow': '#0D47A1'
}

# Components
components = {
    'client': {
        'x': 1, 'y': 5, 'width': 2, 'height': 1.5,
        'label': 'Client Browser\n(HTTP/HTTPS)',
        'color': colors['client']
    },
    'frontend': {
        'x': 4, 'y': 5, 'width': 2, 'height': 1.5,
        'label': 'Frontend\nReact App\nPort: 3000',
        'color': colors['frontend']
    },
    'backend': {
        'x': 7, 'y': 5, 'width': 2, 'height': 1.5,
        'label': 'Backend API\nExpress.js\nPort: 5000',
        'color': colors['backend']
    },
    'database': {
        'x': 10, 'y': 5, 'width': 2, 'height': 1.5,
        'label': 'Database\nPostgreSQL\nPort: 5432',
        'color': colors['database']
    }
}

# Draw components
for key, comp in components.items():
    # Draw box
    box = FancyBboxPatch(
        (comp['x'] - comp['width']/2, comp['y'] - comp['height']/2),
        comp['width'], comp['height'],
        boxstyle="round,pad=0.1",
        facecolor=comp['color'],
        edgecolor='black',
        linewidth=2
    )
    ax.add_patch(box)
    
    # Add label
    ax.text(comp['x'], comp['y'], comp['label'],
            ha='center', va='center',
            fontsize=10, fontweight='bold',
            color=colors['text'])

# Draw arrows (communication flow)
arrows = [
    ('client', 'frontend', 'HTTP/HTTPS\nRequests'),
    ('frontend', 'backend', 'REST API Calls'),
    ('backend', 'database', 'SQL Queries'),
    ('database', 'backend', 'Query Results'),
    ('backend', 'frontend', 'JSON Responses'),
    ('frontend', 'client', 'Rendered UI')
]

# Arrow coordinates mapping
coords = {
    'client': (components['client']['x'] + components['client']['width']/2, 
               components['client']['y']),
    'frontend': (components['frontend']['x'] - components['frontend']['width']/2,
                 components['frontend']['y']),
    'backend': (components['backend']['x'] - components['backend']['width']/2,
                components['backend']['y']),
    'database': (components['database']['x'] - components['database']['width']/2,
                 components['database']['y'])
}

for i, (from_comp, to_comp, label) in enumerate(arrows):
    if from_comp == 'frontend' and to_comp == 'backend':
        # Adjust for two-way arrows
        start = (coords[from_comp][0] + 0.1, coords[from_comp][1])
        end = (coords[to_comp][0] - 0.1, coords[to_comp][1])
    elif from_comp == 'backend' and to_comp == 'frontend':
        # Return arrow
        start = (coords[from_comp][0] + 0.1, coords[from_comp][1])
        end = (coords[to_comp][0] - 0.1, coords[to_comp][1])
    elif from_comp == 'backend' and to_comp == 'database':
        start = (coords[from_comp][0] + components['backend']['width'], 
                 coords[from_comp][1])
        end = (coords[to_comp][0] - 0.1, coords[to_comp][1])
    elif from_comp == 'database' and to_comp == 'backend':
        start = (coords[from_comp][0] + 0.1, coords[from_comp][1])
        end = (coords[to_comp][0] - components['backend']['width'], 
               coords[to_comp][1])
    else:
        start = coords[from_comp]
        end = coords[to_comp]
    
    # Draw arrow
    arrow = FancyArrowPatch(
        start, end,
        arrowstyle='-|>,head_width=0.4,head_length=0.4',
        color=colors['arrow'],
        linewidth=2,
        mutation_scale=20
    )
    ax.add_patch(arrow)
    
    # Add label near arrow
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    
    # Offset label position based on arrow direction
    offset_x = 0
    offset_y = 0.2 if i % 2 == 0 else -0.2
    
    ax.text(mid_x + offset_x, mid_y + offset_y, label,
            ha='center', va='center',
            fontsize=8, fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

# Add title
ax.text(6, 9, 'Multi-Tenant SaaS Architecture Diagram',
        ha='center', va='center',
        fontsize=16, fontweight='bold',
        color='#0D47A1')

# Add subtitle
ax.text(6, 8.5, 'Three-Tier Architecture with Docker Containers',
        ha='center', va='center',
        fontsize=12,
        color='#1976D2')

# Add legend for Docker services
legend_elements = [
    patches.Patch(facecolor=colors['frontend'], edgecolor='black', 
                  label='Frontend Container (React)'),
    patches.Patch(facecolor=colors['backend'], edgecolor='black', 
                  label='Backend Container (Node.js)'),
    patches.Patch(facecolor=colors['database'], edgecolor='black', 
                  label='Database Container (PostgreSQL)'),
]
ax.legend(handles=legend_elements, loc='lower center', 
          bbox_to_anchor=(0.5, 0.02), ncol=3,
          fontsize=9, framealpha=0.9)

# Add authentication flow note
ax.text(6, 1.5, 'Authentication: JWT Tokens | Data Isolation: tenant_id filtering',
        ha='center', va='center',
        fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF3E0', edgecolor='#FF9800'))

plt.tight_layout()
plt.savefig('docs/images/system-architecture.png', dpi=300, bbox_inches='tight')
plt.savefig('docs/images/system-architecture.pdf', bbox_inches='tight')
print("System architecture diagram saved to docs/images/system-architecture.png")