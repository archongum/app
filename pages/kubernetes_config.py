import base64
from dataclasses import dataclass
from io import StringIO
from typing import Optional

import streamlit as st
import yaml
from dotenv import dotenv_values
from st_pages import add_page_title


@dataclass
class Metadata:
    name: str
    namespace: Optional[str] = None
    labels: Optional[dict[str, str]] = None


@dataclass
class YamlBase:
    kind: str = "Secret"
    apiVersion: str = "v1"
    metadata: Metadata = Metadata(name="app-secret")
    type: str = "Opaque"
    data: dict[str, str] = None


def _represent_dataclass(dumper, data):
    return dumper.represent_dict(vars(data))


yaml.add_representer(Metadata, _represent_dataclass)
yaml.add_representer(YamlBase, _represent_dataclass)


ENV_EXAMPLE = """
# DB
DB_URL=mysql+pymysql://username:password@127.0.0.1:3306/test

# S3
CDN_S3_ENDPOINT=https://oss-cn-guangzhou.aliyuncs.com
CDN_S3_BUCKET_NAME=archon
CDN_S3_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxxxx
CDN_S3_ACCESS_KEY_SECRET=yyyyyyyyyyyyyyyyyyyyyy
CDN_S3_BUCKET_URL=https://cdn.example.com
CDN_S3_USE_SSL=true
""".strip()

YAML_EXAMPLE = """
kind: Secret
apiVersion: v1
metadata:
  name: app-secret
  namespace: default
type: Opaque
""".strip()


def _env_to_yaml(env_str: str) -> str:
    # `env` format to `data` field of yaml
    data_list = dotenv_values(stream=StringIO(env_str))

    data_encode_dict = {}
    for k, v in data_list.items():
        v = base64.b64encode(v.encode(encoding="utf-8")).decode(encoding="utf-8")
        data_encode_dict[k] = v

    # Load yaml template and concat with `data`
    yaml_object = YamlBase(**yaml.safe_load(YAML_EXAMPLE))
    yaml_object.data = data_encode_dict
    return yaml.dump(yaml_object, sort_keys=False)


def _yaml_to_env(yaml_str: str) -> str:
    data_dict = YamlBase(**yaml.safe_load(yaml_str)).data
    env_str = ""
    for key, value in data_dict.items():
        value = base64.b64decode(value.encode(encoding="utf-8")).decode(
            encoding="utf-8"
        )
        env_str += f"{key}={value}\n"
    return env_str


def main():
    add_page_title(layout="wide")

    if st.session_state.get("c_text_env") is None:
        st.session_state.c_text_env = ENV_EXAMPLE
    if st.session_state.get("c_text_yaml") is None:
        st.session_state.c_text_yaml = _env_to_yaml(ENV_EXAMPLE)

    def _on_env_to_yaml():
        st.session_state.c_text_yaml = _env_to_yaml(st.session_state.c_text_env)

    def _on_yaml_to_env():
        st.session_state.c_text_env = _yaml_to_env(st.session_state.c_text_yaml)

    c_text_env, c_text_yaml = st.columns([5, 5])
    with c_text_env:
        st.text_area("ENV", height=473, key="c_text_env", on_change=_on_env_to_yaml)
    with c_text_yaml:
        st.text_area("YAML", height=473, key="c_text_yaml", on_change=_on_yaml_to_env)

    st.markdown(
        r"""
> Tips: Change ENV or YAML then press `Ctrl + Enter`.
>
> Or using buttoms blow:
""".strip()
    )
    st.button("ENV -> YAML", on_click=_on_env_to_yaml)
    st.button("YAML -> ENV", on_click=_on_yaml_to_env)


if __name__ == "__main__":
    main()
