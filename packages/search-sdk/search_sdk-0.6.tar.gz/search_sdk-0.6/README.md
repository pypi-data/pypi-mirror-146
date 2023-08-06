### 安装方法
pip install search-sdk
pip install alibabacloud_ha3engine

### 使用
    from search_sdk import table
    t = table.Table(
        endpoint="",
        instance_id="",
        access_user_name="",
        access_pass_word="",
        table_name="",
        pk_field="",
        data_source_name="",
        hash_field="",
    )