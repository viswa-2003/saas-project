import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors for different table types
colors = {
    'core': '#E8F5E9',      # Green for core tables
    'auth': '#E3F2FD',      # Blue for auth tables
    'audit': '#FFF3E0',     # Orange for audit tables
    'text': '#1B5E20',      # Dark green for text
    'pk': '#4CAF50',        # Green for primary keys
    'fk': '#2196F3',        # Blue for foreign keys
    'constraint': '#FF9800' # Orange for constraints
}

# Table positions (centered coordinates)
tables = {
    'tenants': {
        'x': 4, 'y': 9, 'width': 3.5, 'height': 2.5,
        'color': colors['core'],
        'title': 'tenants',
        'columns': [
            ('id', 'PK', 'UUID'),
            ('name', '', 'VARCHAR(255)'),
            ('subdomain', 'UNIQUE', 'VARCHAR(100)'),
            ('status', '', 'ENUM'),
            ('subscription_plan', '', 'ENUM'),
            ('max_users', '', 'INTEGER'),
            ('max_projects', '', 'INTEGER'),
            ('created_at', '', 'TIMESTAMP'),
            ('updated_at', '', 'TIMESTAMP')
        ]
    },
    'users': {
        'x': 8, 'y': 9, 'width': 3.5, 'height': 3,
        'color': colors['auth'],
        'title': 'users',
        'columns': [
            ('id', 'PK', 'UUID'),
            ('tenant_id', 'FK → tenants.id', 'UUID'),
            ('email', '', 'VARCHAR(255)'),
            ('password_hash', '', 'VARCHAR(255)'),
            ('full_name', '', 'VARCHAR(255)'),
            ('role', '', 'ENUM'),
            ('is_active', '', 'BOOLEAN'),
            ('created_at', '', 'TIMESTAMP'),
            ('updated_at', '', 'TIMESTAMP'),
            ('', 'UNIQUE(tenant_id, email)', 'CONSTRAINT')
        ]
    },
    'projects': {
        'x': 12, 'y': 9, 'width': 3.5, 'height': 2.5,
        'color': colors['core'],
        'title': 'projects',
        'columns': [
            ('id', 'PK', 'UUID'),
            ('tenant_id', 'FK → tenants.id', 'UUID'),
            ('name', '', 'VARCHAR(255)'),
            ('description', '', 'TEXT'),
            ('status', '', 'ENUM'),
            ('created_by', 'FK → users.id', 'UUID'),
            ('created_at', '', 'TIMESTAMP'),
            ('updated_at', '', 'TIMESTAMP')
        ]
    },
    'tasks': {
        'x': 8, 'y': 5, 'width': 3.5, 'height': 3,
        'color': colors['core'],
        'title': 'tasks',
        'columns': [
            ('id', 'PK', 'UUID'),
            ('project_id', 'FK → projects.id', 'UUID'),
            ('tenant_id', 'FK → tenants.id', 'UUID'),
            ('title', '', 'VARCHAR(255)'),
            ('description', '', 'TEXT'),
            ('status', '', 'ENUM'),
            ('priority', '', 'ENUM'),
            ('assigned_to', 'FK → users.id', 'UUID'),
            ('due_date', '', 'DATE'),
            ('created_at', '', 'TIMESTAMP'),
            ('updated_at', '', 'TIMESTAMP')
        ]
    },
    'audit_logs': {
        'x': 4, 'y': 5, 'width': 3.5, 'height': 2.5,
        'color': colors['audit'],
        'title': 'audit_logs',
        'columns': [
            ('id', 'PK', 'UUID'),
            ('tenant_id', 'FK → tenants.id', 'UUID'),
            ('user_id', 'FK → users.id', 'UUID'),
            ('action', '', 'VARCHAR(100)'),
            ('entity_type', '', 'VARCHAR(50)'),
            ('entity_id', '', 'UUID'),
            ('ip_address', '', 'VARCHAR(45)'),
            ('created_at', '', 'TIMESTAMP')
        ]
    }
}

# Draw tables
for table_name, table_data in tables.items():
    x, y = table_data['x'], table_data['y']
    width, height = table_data['width'], table_data['height']
    
    # Draw table box
    box = FancyBboxPatch(
        (x - width/2, y - height/2),
        width, height,
        boxstyle="round,pad=0.1",
        facecolor=table_data['color'],
        edgecolor='black',
        linewidth=2
    )
    ax.add_patch(box)
    
    # Draw table header
    header_height = 0.3
    header_box = patches.Rectangle(
        (x - width/2, y - height/2 + height - header_height),
        width, header_height,
        facecolor='#2E7D32' if table_data['color'] == colors['core'] else 
                 '#1565C0' if table_data['color'] == colors['auth'] else
                 '#EF6C00',
        edgecolor='black',
        linewidth=1
    )
    ax.add_patch(header_box)
    
    # Add table title
    ax.text(x, y - height/2 + height - header_height/2,
            table_data['title'].upper(),
            ha='center', va='center',
            fontsize=11, fontweight='bold',
            color='white')
    
    # Add columns
    column_height = 0.25
    start_y = y + height/2 - header_height - column_height
    
    for i, (col_name, col_type, col_datatype) in enumerate(table_data['columns']):
        col_y = start_y - i * column_height
        
        # Draw column background
        col_bg = patches.Rectangle(
            (x - width/2 + 0.05, col_y - column_height + 0.05),
            width - 0.1, column_height - 0.05,
            facecolor='white',
            edgecolor='lightgray',
            linewidth=0.5,
            alpha=0.7
        )
        ax.add_patch(col_bg)
        
        # Column name with type indicator
        if col_type == 'PK':
            col_text = f"🔑 {col_name}"
            col_color = colors['pk']
        elif 'FK' in col_type:
            col_text = f"🔗 {col_name}"
            col_color = colors['fk']
        elif 'CONSTRAINT' in col_type:
            col_text = f"⚡ {col_name}"
            col_color = colors['constraint']
        else:
            col_text = f"• {col_name}"
            col_color = 'black'
        
        # Column name
        ax.text(x - width/2 + 0.15, col_y - column_height/2,
                col_text,
                ha='left', va='center',
                fontsize=9, fontweight='bold',
                color=col_color)
        
        # Column type/datatype
        type_text = col_type if col_type and not col_datatype else f"{col_type} {col_datatype}" if col_type else col_datatype
        ax.text(x + width/2 - 0.15, col_y - column_height/2,
                type_text,
                ha='right', va='center',
                fontsize=8,
                color='#666666',
                fontstyle='italic')

# Draw relationships (arrows)
relationships = [
    # One-to-Many: tenants → users
    ('tenants', 'users', '1', 'N', 'tenant_id'),
    # One-to-Many: tenants → projects
    ('tenants', 'projects', '1', 'N', 'tenant_id'),
    # One-to-Many: tenants → audit_logs
    ('tenants', 'audit_logs', '1', 'N', 'tenant_id'),
    # One-to-Many: users → projects (created_by)
    ('users', 'projects', '1', 'N', 'created_by'),
    # One-to-Many: users → tasks (assigned_to)
    ('users', 'tasks', '1', 'N', 'assigned_to'),
    # One-to-Many: users → audit_logs
    ('users', 'audit_logs', '1', 'N', 'user_id'),
    # One-to-Many: projects → tasks
    ('projects', 'tasks', '1', 'N', 'project_id'),
    # One-to-Many: tenants → tasks
    ('tenants', 'tasks', '1', 'N', 'tenant_id')
]

# Draw relationship lines
for from_table, to_table, from_card, to_card, fk_column in relationships:
    from_x = tables[from_table]['x'] + tables[from_table]['width']/2
    from_y = tables[from_table]['y']
    to_x = tables[to_table]['x'] - tables[to_table]['width']/2
    to_y = tables[to_table]['y']
    
    # Adjust positions to avoid overlap
    if from_table == 'tenants' and to_table == 'users':
        from_y -= 0.5
        to_y -= 0.5
    elif from_table == 'tenants' and to_table == 'projects':
        from_y += 0.5
        to_y += 0.5
    
    # Draw line
    arrow = FancyArrowPatch(
        (from_x, from_y), (to_x, to_y),
        arrowstyle='-|>,head_width=0.3,head_length=0.3',
        color='#666666',
        linewidth=1.5,
        linestyle='--' if 'audit' in to_table else '-',
        alpha=0.7,
        connectionstyle="arc3,rad=0.1"
    )
    ax.add_patch(arrow)
    
    # Add cardinality labels
    mid_x = (from_x + to_x) / 2
    mid_y = (from_y + to_y) / 2
    
    # Adjust label position
    label_x = mid_x + 0.1
    label_y = mid_y + 0.1
    
    ax.text(label_x, label_y, f"{from_card}:{to_card}",
            ha='center', va='center',
            fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
    
    # Add FK column name
    fk_x = (from_x + to_x) / 2
    fk_y = (from_y + to_y) / 2 - 0.2
    
    ax.text(fk_x, fk_y, fk_column,
            ha='center', va='center',
            fontsize=7, fontstyle='italic',
            color='#2196F3')

# Add title
ax.text(8, 11.5, 'Database Entity Relationship Diagram (ERD)',
        ha='center', va='center',
        fontsize=18, fontweight='bold',
        color='#1B5E20')

# Add subtitle
ax.text(8, 11, 'Multi-Tenant SaaS Platform - PostgreSQL Schema',
        ha='center', va='center',
        fontsize=12,
        color='#388E3C')

# Add legend
legend_elements = [
    patches.Patch(facecolor=colors['core'], edgecolor='black', 
                  label='Core Tables (Business Data)'),
    patches.Patch(facecolor=colors['auth'], edgecolor='black', 
                  label='Authentication Tables'),
    patches.Patch(facecolor=colors['audit'], edgecolor='black', 
                  label='Audit Logging Tables'),
    patches.Patch(facecolor='white', edgecolor='black',
                  label='🔑 = Primary Key'),
    patches.Patch(facecolor='white', edgecolor='black',
                  label='🔗 = Foreign Key'),
    patches.Patch(facecolor='white', edgecolor='black',
                  label='⚡ = Constraint'),
]

ax.legend(handles=legend_elements, loc='lower center',
          bbox_to_anchor=(0.5, 0.01), ncol=2,
          fontsize=9, framealpha=0.9)

# Add multi-tenancy note
tenancy_note = """Multi-Tenancy Implementation:
• All tables (except super_admin) have tenant_id column
• Foreign keys cascade delete for data integrity
• Unique constraint: (tenant_id, email) in users table
• Indexes on all tenant_id columns for performance
• Super admin users have tenant_id = NULL"""

ax.text(13, 3, tenancy_note,
        ha='left', va='top',
        fontsize=9,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#F5F5F5', edgecolor='#9E9E9E'))

plt.tight_layout()
plt.savefig('docs/images/database-erd.png', dpi=300, bbox_inches='tight')
plt.savefig('docs/images/database-erd.pdf', bbox_inches='tight')
print("Database ERD diagram saved to docs/images/database-erd.png")