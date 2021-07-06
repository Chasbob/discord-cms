FROM postgres:13

HEALTHCHECK --interval=5s --timeout=5s --retries=12 CMD \
    pg_isready -q -d $POSTGRES_DB -U $POSTGRES_USER
