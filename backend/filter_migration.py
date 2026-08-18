import re

with open("alembic/versions/b688031139ce_add_bible_engine_models.py", "r") as f:
    content = f.read()

# We need to find all op.create_table(...) blocks.
# And all op.create_index(...) blocks.
# We will only keep the ones that mention the bible tables.

bible_tables = [
    'bible_translations', 'bible_books', 'bible_chapters', 'bible_verses', 
    'cross_references', 'bible_topics', 'topic_verses', 'bible_versions', 
    'bible_characters', 'character_references', 'book_summaries', 
    'chapter_summaries', 'verse_notes', 'verse_history'
]

def filter_upgrade_downgrade(func_str, op_type):
    # Regex to find op.create_table( 'table_name', ... )
    # This is tricky because it spans multiple lines.
    lines = func_str.split("\n")
    out_lines = []
    skip = False
    for line in lines:
        if "op.create_table(" in line or "op.drop_table(" in line:
            # find table name
            match = re.search(r"op\.(create_table|drop_table)\('([^']+)'", line)
            if match:
                table_name = match.group(2)
                if table_name not in bible_tables:
                    skip = True
                else:
                    skip = False
        elif "op.create_index(" in line or "op.drop_index(" in line:
            match = re.search(r"op\.(create_index|drop_index)\('[^']+', '([^']+)'", line)
            if match:
                table_name = match.group(2)
                if table_name not in bible_tables:
                    skip = True
                else:
                    skip = False
        
        if not skip:
            out_lines.append(line)
            
        # if skip is True, we need to know when to stop skipping.
        # usually op.create_table ends with a `)` on a line by itself or `    )`
        if skip and line.strip() == ")":
            skip = False
            
    return "\n".join(out_lines)

upgrade_str = content.split("def upgrade() -> None:")[1].split("def downgrade() -> None:")[0]
downgrade_str = content.split("def downgrade() -> None:")[1]

new_upgrade = filter_upgrade_downgrade(upgrade_str, "upgrade")
new_downgrade = filter_upgrade_downgrade(downgrade_str, "downgrade")

new_content = content.split("def upgrade() -> None:")[0] + "def upgrade() -> None:" + new_upgrade + "def downgrade() -> None:" + new_downgrade

with open("alembic/versions/b688031139ce_add_bible_engine_models.py", "w") as f:
    f.write(new_content)

print("Filtered migration!")
