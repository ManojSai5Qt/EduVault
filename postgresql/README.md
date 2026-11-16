# PostgreSQL files

## Full schema and data backup

`EduVault_backup.sql` is the project's full PostgreSQL dump. It contains the SQL used to create the tables and related database objects, plus the saved table data.

To find the table definitions, open the file and search for:

- `CREATE TABLE public.students`
- `CREATE TABLE public.courses`
- `CREATE TABLE public.departments`
- `CREATE TABLE public.enrollments`
- `CREATE TABLE public.grades`

The dump also defines instructors, course prerequisites, student certifications and student languages, along with sequences, constraints and indexes. It is a full restore file, not a schema-only file.

## Other SQL examples

- `concurrency/`: transaction, isolation, MVCC, lock, 2PC and concurrency-control examples.
- `replication/`: physical replication, logical replication and partitioning examples.
- `setup/restore.sh`: shell helper for restoring the full dump from the repository root.

The backup is kept at this location so the existing restore script continues to work.
