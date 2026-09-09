"""Initial schema migration — all tables from project PDF data model.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-09-09

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('email', sa.String(200), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('password_hash', sa.String(200), nullable=False),
        sa.Column('role', sa.Enum('DONOR', 'NGO', 'DRIVER', 'ADMIN', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'])

    # Donors
    op.create_table(
        'donors',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('user_id', sa.String(50), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('organisation_name', sa.String(200), nullable=False),
        sa.Column('address', sa.Text, nullable=False),
        sa.Column('location', sa.String(200), nullable=False),
        sa.Column('contact_person', sa.String(200), nullable=False),
        sa.Column('verification_status', sa.String(50), nullable=False),
        sa.Column('daily_waste_category', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_donors_user_id', 'donors', ['user_id'])

    # NGOs
    op.create_table(
        'ngos',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('user_id', sa.String(50), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('organisation_name', sa.String(200), nullable=False),
        sa.Column('address', sa.Text, nullable=False),
        sa.Column('location', sa.String(200), nullable=False),
        sa.Column('storage_capacity_kg', sa.Float, nullable=False),
        sa.Column('available_capacity_kg', sa.Float, nullable=False),
        sa.Column('operating_start', sa.String(10), nullable=False),
        sa.Column('operating_end', sa.String(10), nullable=False),
        sa.Column('verification_status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='ngoverificationstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_ngos_user_id', 'ngos', ['user_id'])
    op.create_index('ix_ngos_verification_status', 'ngos', ['verification_status'])

    # NGO Food Categories
    op.create_table(
        'ngo_food_categories',
        sa.Column('ngo_id', sa.String(50), sa.ForeignKey('ngos.id'), primary_key=True),
        sa.Column('food_category', sa.String(50), primary_key=True),
        sa.Column('accepted', sa.Boolean, nullable=False, default=True),
    )

    # NGO Demand
    op.create_table(
        'ngo_demand',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('ngo_id', sa.String(50), sa.ForeignKey('ngos.id'), nullable=False),
        sa.Column('food_category', sa.String(50), nullable=False),
        sa.Column('required_quantity_kg', sa.Float, nullable=False),
        sa.Column('priority', sa.String(20), nullable=False),
        sa.Column('valid_until', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_ngo_demand_ngo_id', 'ngo_demand', ['ngo_id'])

    # Donations
    op.create_table(
        'donations',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('donor_id', sa.String(50), sa.ForeignKey('donors.id'), nullable=False),
        sa.Column('food_category', sa.String(50), nullable=False),
        sa.Column('food_name', sa.String(200), nullable=False),
        sa.Column('quantity_kg', sa.Float, nullable=False),
        sa.Column('prepared_at', sa.DateTime, nullable=False),
        sa.Column('available_from', sa.DateTime, nullable=False),
        sa.Column('expiry_time', sa.DateTime, nullable=False),
        sa.Column('pickup_location', sa.String(200), nullable=False),
        sa.Column('special_requirements', sa.Text, nullable=True),
        sa.Column('status', sa.Enum('AVAILABLE', 'MATCHING', 'MATCHED', 'ACCEPTED', 'DRIVER_ASSIGNED',
                                     'PICKUP_STARTED', 'PICKED_UP', 'IN_TRANSIT', 'DELIVERED',
                                     'PARTIALLY_DELIVERED', 'NO_MATCH_FOUND', 'REJECTED', 'EXPIRED',
                                     'CANCELLED', 'DRIVER_ISSUE', name='donationstatus'), nullable=False),
        sa.Column('matched_ngo_id', sa.String(50), sa.ForeignKey('ngos.id'), nullable=True),
        sa.Column('match_score', sa.Float, nullable=True),
        sa.Column('weights_version_id', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_donations_donor_id', 'donations', ['donor_id'])
    op.create_index('ix_donations_food_category', 'donations', ['food_category'])
    op.create_index('ix_donations_expiry_time', 'donations', ['expiry_time'])
    op.create_index('ix_donations_status', 'donations', ['status'])
    op.create_index('ix_donations_matched_ngo_id', 'donations', ['matched_ngo_id'])
    op.create_index('ix_donations_created_at', 'donations', ['created_at'])

    # Vehicles
    op.create_table(
        'vehicles',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('driver_id', sa.String(50), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('capacity_kg', sa.Float, nullable=False),
        sa.Column('current_location', sa.String(200), nullable=False),
        sa.Column('availability_status', sa.String(50), nullable=False),
    )
    op.create_index('ix_vehicles_driver_id', 'vehicles', ['driver_id'])
    op.create_index('ix_vehicles_availability_status', 'vehicles', ['availability_status'])

    # Deliveries
    op.create_table(
        'deliveries',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('donation_id', sa.String(50), sa.ForeignKey('donations.id'), nullable=False),
        sa.Column('ngo_id', sa.String(50), sa.ForeignKey('ngos.id'), nullable=False),
        sa.Column('driver_id', sa.String(50), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('pickup_time', sa.DateTime, nullable=True),
        sa.Column('estimated_delivery_time', sa.DateTime, nullable=True),
        sa.Column('actual_pickup_time', sa.DateTime, nullable=True),
        sa.Column('actual_delivery_time', sa.DateTime, nullable=True),
        sa.Column('route_distance_km', sa.Float, nullable=True),
        sa.Column('estimated_duration_min', sa.Integer, nullable=True),
        sa.Column('status', sa.Enum('DRIVER_ASSIGNED', 'PICKUP_STARTED', 'PICKED_UP', 'IN_TRANSIT',
                                     'DELIVERED', 'PARTIALLY_DELIVERED', 'CANCELLED', 'DRIVER_ISSUE',
                                     name='deliverystatus'), nullable=False),
    )
    op.create_index('ix_deliveries_donation_id', 'deliveries', ['donation_id'])
    op.create_index('ix_deliveries_ngo_id', 'deliveries', ['ngo_id'])
    op.create_index('ix_deliveries_driver_id', 'deliveries', ['driver_id'])
    op.create_index('ix_deliveries_status', 'deliveries', ['status'])
    op.create_index('ix_deliveries_actual_delivery_time', 'deliveries', ['actual_delivery_time'])

    # Handover Records
    op.create_table(
        'handover_records',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('donation_id', sa.String(50), sa.ForeignKey('donations.id'), nullable=False),
        sa.Column('delivery_id', sa.String(50), sa.ForeignKey('deliveries.id'), nullable=False),
        sa.Column('donor_confirmation', sa.Boolean, nullable=False),
        sa.Column('ngo_confirmation', sa.Boolean, nullable=False),
        sa.Column('pickup_timestamp', sa.DateTime, nullable=False),
        sa.Column('delivery_timestamp', sa.DateTime, nullable=False),
        sa.Column('quantity_handed_over', sa.Float, nullable=False),
        sa.Column('donor_signature', sa.String(500), nullable=True),
        sa.Column('recipient_signature', sa.String(500), nullable=True),
        sa.Column('disclaimer_version', sa.String(50), nullable=False),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_handover_records_donation_id', 'handover_records', ['donation_id'])
    op.create_index('ix_handover_records_delivery_id', 'handover_records', ['delivery_id'])

    # NGO Verification Documents
    op.create_table(
        'ngo_verification_documents',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('ngo_id', sa.String(50), sa.ForeignKey('ngos.id'), nullable=False),
        sa.Column('document_type', sa.String(100), nullable=False),
        sa.Column('file_url', sa.String(500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_ngo_verification_documents_ngo_id', 'ngo_verification_documents', ['ngo_id'])

    # Audit Logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.String(50), nullable=False),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('payload', sa.JSON, nullable=False),
        sa.Column('record_hash', sa.String(64), nullable=False),
        sa.Column('previous_hash', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )
    op.create_index('ix_audit_logs_entity_type', 'audit_logs', ['entity_type'])
    op.create_index('ix_audit_logs_entity_id', 'audit_logs', ['entity_id'])
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'])


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('ngo_verification_documents')
    op.drop_table('handover_records')
    op.drop_table('deliveries')
    op.drop_table('vehicles')
    op.drop_table('donations')
    op.drop_table('ngo_demand')
    op.drop_table('ngo_food_categories')
    op.drop_table('ngos')
    op.drop_table('donors')
    op.drop_table('users')

    # Drop enums
    sa.Enum(name='donationstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='deliverystatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='ngoverificationstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)
