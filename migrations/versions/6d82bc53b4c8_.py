"""empty message

Revision ID: 6d82bc53b4c8
Revises: 
Create Date: 2022-06-09 19:23:46.545065

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6d82bc53b4c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Website_Word_Counter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('word_count_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('word_counter',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('salted_hash', sa.String(), nullable=False),
    sa.Column('encrypted_word', sqlalchemy_utils.types.encrypted.encrypted_type.EncryptedType(), nullable=True),
    sa.Column('frequency', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('salted_hash')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('word_counter')
    op.drop_table('Website_Word_Counter')
    # ### end Alembic commands ###