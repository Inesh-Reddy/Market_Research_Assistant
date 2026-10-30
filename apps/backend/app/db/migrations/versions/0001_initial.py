"""initial
Revision ID: 0001
"""
from alembic import op

revision="0001"; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
    op.execute("CREATE TABLE IF NOT EXISTS conversations (id VARCHAR(36) PRIMARY KEY, created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ)")
    op.execute("CREATE TABLE IF NOT EXISTS executions (id VARCHAR(36) PRIMARY KEY, conversation_id VARCHAR(36), question TEXT, ticker VARCHAR(16), status VARCHAR(32), final_response TEXT, created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ)")
    op.execute("CREATE TABLE IF NOT EXISTS agent_executions (id VARCHAR(36) PRIMARY KEY, execution_id VARCHAR(36), agent_name VARCHAR(64), status VARCHAR(32), created_at TIMESTAMPTZ)")
    op.execute("CREATE TABLE IF NOT EXISTS execution_events (id VARCHAR(36) PRIMARY KEY, execution_id VARCHAR(36), conversation_id VARCHAR(36), event_type VARCHAR(64), agent_name VARCHAR(64), payload JSON, created_at TIMESTAMPTZ)")
    op.execute("CREATE TABLE IF NOT EXISTS agent_results (id VARCHAR(36) PRIMARY KEY, execution_id VARCHAR(36), agent_name VARCHAR(64), result_json JSON, created_at TIMESTAMPTZ)")
    op.execute("CREATE TABLE IF NOT EXISTS prompt_versions (id VARCHAR(36) PRIMARY KEY, agent_name VARCHAR(64), version VARCHAR(32), content TEXT, created_at TIMESTAMPTZ)")
def downgrade():
    for t in ["prompt_versions","agent_results","execution_events","agent_executions","executions","conversations"]: op.execute(f"DROP TABLE IF EXISTS {t}")
