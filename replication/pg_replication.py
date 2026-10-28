import pandas as pd

class PGReplicationManager:
    """
    Manages PostgreSQL Physical Streaming Replication and Logical Replication architectures.
    """

    COMPARISON_DATA = [
        {"Feature": "Replication Level", "Physical Streaming Replication": "Physical block-level (WAL binary stream)", "Logical Replication": "Logical table-level (Decoded SQL row events)"},
        {"Feature": "Granularity", "Physical Streaming Replication": "Entire database cluster (All DBs, tables, catalogs)", "Logical Replication": "Selective per-table or table subsets with WHERE row filters"},
        {"Feature": "Target Node State", "Physical Streaming Replication": "Read-Only (Hot Standby)", "Logical Replication": "Read-Write (Can accept independent writes & custom indexes)"},
        {"Feature": "Postgres Version Compatibility", "Physical Streaming Replication": "Must be exact same major version and architecture", "Logical Replication": "Cross-major version compatible (e.g. PG 14 -> PG 17)"},
        {"Feature": "DDL Schema Changes", "Physical Streaming Replication": "Automatically replicated via WAL byte-stream", "Logical Replication": "DDL is NOT automatically replicated; schemas must match"},
        {"Feature": "Primary wal_level Config", "Physical Streaming Replication": "wal_level = replica", "Logical Replication": "wal_level = logical"},
        {"Feature": "Replication Slot Type", "Physical Streaming Replication": "Physical slot (pg_create_physical_replication_slot)", "Logical Replication": "Logical slot (using pgoutput plugin)"},
        {"Feature": "Best Use Cases", "Physical Streaming Replication": "High Availability (HA), Disaster Recovery, Read Replicas", "Logical Replication": "Data Warehousing, Microservice data sharing, Zero-downtime upgrades, CDC"},
    ]

    @staticmethod
    def get_comparison_df():
        return pd.DataFrame(PGReplicationManager.COMPARISON_DATA)

    @staticmethod
    def get_simulated_pg_stat_replication():
        """
        Simulates live output of SELECT * FROM pg_stat_replication.
        """
        data = [
            {
                "pid": 14201,
                "usename": "replicator",
                "application_name": "standby_node_us_east",
                "client_addr": "10.0.1.25",
                "state": "streaming",
                "sync_state": "sync",
                "sync_priority": 1,
                "sent_lsn": "0/16B38D0",
                "write_lsn": "0/16B38D0",
                "flush_lsn": "0/16B38D0",
                "replay_lsn": "0/16B3880",
                "write_lag": "00:00:00.002",
                "flush_lag": "00:00:00.004",
                "replay_lag": "00:00:00.012"
            },
            {
                "pid": 14208,
                "usename": "replicator",
                "application_name": "standby_node_eu_central",
                "client_addr": "10.0.2.80",
                "state": "streaming",
                "sync_state": "async",
                "sync_priority": 2,
                "sent_lsn": "0/16B38D0",
                "write_lsn": "0/16B3898",
                "flush_lsn": "0/16B3898",
                "replay_lsn": "0/16B3800",
                "write_lag": "00:00:00.085",
                "flush_lag": "00:00:00.091",
                "replay_lag": "00:00:00.145"
            }
        ]
        return pd.DataFrame(data)

    @staticmethod
    def get_simulated_pg_stat_subscription():
        """
        Simulates output of SELECT * FROM pg_stat_subscription for Logical Replication.
        """
        data = [
            {
                "subid": 16420,
                "subname": "eduvault_analytics_sub",
                "pid": 19280,
                "relid": "All Tables",
                "received_lsn": "0/16B38D0",
                "last_msg_send_time": "2026-10-28 23:15:00.120+00",
                "last_msg_receipt_time": "2026-10-28 23:15:00.122+00",
                "latest_end_lsn": "0/16B38D0",
                "latest_end_time": "2026-10-28 23:15:00.125+00"
            }
        ]
        return pd.DataFrame(data)
