import streamlit as st
from omymodels import create_models
from st_pages import add_page_title

DDL_EXAMPLE = r"""
CREATE TABLE "material" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar NOT NULL,
  "description" text,
  "link" varchar NOT NULL,
  "type" integer NOT NULL,
  "additional_properties" json,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp
);
""".strip()


def main():
    add_page_title(layout="wide")

    st.markdown(
        r"""
    > 💪Powered by: https://github.com/xnuinside/omymodels
    """.strip()
    )

    c_selectbox_models_type = st.selectbox(
        "Model Type",
        options=["gino", "sqlalchemy", "sqlalchemy_core", "pydantic", "dataclass"],
        index=1,
    )

    c_text_ddl, c_code_result = st.columns([5, 6])

    ddl = c_text_ddl.text_area("DDL", value=DDL_EXAMPLE, height=473)

    # ddl: Optional[str] = (None,)
    # ddl_path: Optional[str] = (None,)
    # dump: bool = (True,)
    # dump_path: str = ("models.py",)
    # singular: bool = (False,)
    # naming_exceptions: Optional[List] = (None,)
    # models_type: str = ("gino",)
    # schema_global: Optional[bool] = (True,)
    # defaults_off: Optional[bool] = (False,)
    # exit_silent: Optional[bool] = (False,)
    # no_auto_snake_case: Optional[bool] = False

    result = create_models(
        ddl,
        models_type=c_selectbox_models_type,
        dump=False,
    )

    c_code_result.code(result["code"], language="python", line_numbers=True)


if __name__ == "__main__":
    main()
