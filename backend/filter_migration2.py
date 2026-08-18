import re

with open("alembic/versions/b688031139ce_add_bible_engine_models.py", "r") as f:
    content = f.read()

bible_tables = [
    'bible_translations', 'bible_books', 'bible_chapters', 'bible_verses', 
    'cross_references', 'bible_topics', 'topic_verses', 'bible_versions', 
    'bible_characters', 'character_references', 'book_summaries', 
    'chapter_summaries', 'verse_notes', 'verse_history'
]

def filter_upgrade_downgrade(func_str, op_type):
    lines = func_str.split("\n")
    out_lines = []
    skip = False
    for line in lines:
        # Match create/drop table
        if "op.create_table(" in line or "op.drop_table(" in line:
            match = re.search(r"op\.(create_table|drop_table)\('([^']+)'", line)
            if match:
                table_name = match.group(2)
                if table_name not in bible_tables:
                    skip = True
                else:
                    skip = False
        
        # Match create/drop index. They are one line.
        elif "op.create_index(" in line or "op.drop_index(" in line:
            # table_name can be in op.create_index(..., 'table_name', ...) or table_name='...'
            match1 = re.search(r"op\.(create_index|drop_index)\([^,]+, '([^']+)'", line)
            match2 = re.search(r"table_name='([^']+)'", line)
            table_name = None
            if match1:
                table_name = match1.group(2)
            elif match2:
                table_name = match2.group(1)
                
            if table_name and table_name not in bible_tables:
                continue # Skip this line
        
        # also skip ai_usage
        elif "ai_usage" in line:
            if "op.create_table" in line or "op.create_index" in line:
                continue
                
        if not skip:
            out_lines.append(line)
            
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

print("Filtered migration again!")
