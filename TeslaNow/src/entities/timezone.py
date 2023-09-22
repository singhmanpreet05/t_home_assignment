class Timezone:
    def __init__(self, name, is_custom, offset, created_at, updated_at):
        self.name = name
        self.is_custom = is_custom
        self.offset = offset
        self.created_at = created_at
        self.updated_at = updated_at