# import traceback
# import pandas as pd
# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import io
# from graph.pipeline import cbam_pipeline
# from graph.state import CBAMState

# app = FastAPI(title="CBAM PILOT AI")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


# @app.get("/")
# def health_check():
#     return {"status": "CBAM Pilot AI is running"}


# @app.post("/analyze")
# async def analyze_imports(file: UploadFile = File(...)):

#     try:
#         # Step 1: Read uploaded file
#         contents = await file.read()

#         # Step 2: Load into pandas based on file type
#         filename = (file.filename or "").lower()
#         if filename.endswith(".csv"):
#             df = pd.read_csv(io.BytesIO(contents))
#         elif filename.endswith((".xls", ".xlsx")):
#             df = pd.read_excel(io.BytesIO(contents))
#         else:
#             raise HTTPException(status_code=400, detail="Only CSV and Excel files allowed")

#         # Step 3: Check required columns exist
#         required_columns = ["product_description", "country_of_origin", "volume_tonnes"]
#         for col in required_columns:
#             if col not in df.columns:
#                 raise HTTPException(status_code=400, detail=f"Missing required column: {col}")

#         # Step 4: Process each row through LangGraph pipeline
#         results = []

#         for _, row in df.iterrows():

#             input_state: CBAMState = {
#                 "product_description": str(row["product_description"]),
#                 "country_of_origin": str(row["country_of_origin"]),
#                 "volume_tonnes": float(row["volume_tonnes"]),
#                 "supplier": str(row.get("supplier", "")),
#                 "cn_code": None,
#                 "category": None,
#                 "classification_note": None,
#                 "cbam_covered": None,
#                 "emission_factor": None,
#                 "embedded_emissions": None,
#                 "ets_price": None,
#                 "estimated_cbam_cost": None,
#                 "status": None,
#             }

#             output = cbam_pipeline.invoke(input_state)

#             results.append({
#                 "product_description": output.get("product_description"),
#                 "country_of_origin": output.get("country_of_origin"),
#                 "volume_tonnes": output.get("volume_tonnes"),
#                 "cn_code": output.get("cn_code"),
#                 "category": output.get("category"),
#                 "cbam_covered": output.get("cbam_covered"),
#                 "emission_factor": output.get("emission_factor"),
#                 "embedded_emissions": output.get("embedded_emissions"),
#                 "ets_price": output.get("ets_price"),
#                 "estimated_cbam_cost": output.get("estimated_cbam_cost"),
#                 "status": output.get("status"),
#                 "classification_note": output.get("classification_note"),
#             })

#         # Step 5: Return all results
#         return {
#             "total_imports": len(results),
#             "items": results
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


import traceback
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import io
from graph.pipeline import cbam_pipeline
from graph.state import CBAMState

app = FastAPI(title="CBAM PILOT AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def health_check():
    return {"status": "CBAM Pilot AI is running"}


@app.post("/analyze")
async def analyze_imports(file: UploadFile = File(...)):

    try:
        # Step 1: Read uploaded file
        contents = await file.read()

        # Step 2: Load into pandas
        filename = (file.filename or "").lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Only CSV and Excel files allowed")

        # Step 3: Normalize column names
        # lowercase + strip spaces so any variation works
        df.columns = [col.strip().lower() for col in df.columns]

        # Step 4: Map alternative column names to our standard names
        column_mapping = {
            "weight_tonnes": "volume_tonnes",
            "weight": "volume_tonnes",
            "tonnes": "volume_tonnes",
            "supplier_country": "country_of_origin",
            "origin": "country_of_origin",
            "country": "country_of_origin",
            "importer": "product_description",
            "product": "product_description",
            "description": "product_description",
            "goods": "product_description",
            "cn_code": "cn_code_input",   # keep cn_code separate
        }
        df = df.rename(columns=column_mapping)

        # Step 5: Fill missing columns with defaults
        if "product_description" not in df.columns:
            # use cn_code_input as description if no product description
            if "cn_code_input" in df.columns:
                df["product_description"] = df["cn_code_input"]
            else:
                df["product_description"] = "Unknown Product"

        if "country_of_origin" not in df.columns:
            df["country_of_origin"] = "Unknown"

        if "volume_tonnes" not in df.columns:
            df["volume_tonnes"] = 0.0

        # Step 6: Process each row through LangGraph pipeline
        results = []

        for _, row in df.iterrows():

            input_state: CBAMState = {
                "product_description": str(row.get("product_description", "Unknown")),
                "country_of_origin": str(row.get("country_of_origin", "Unknown")),
                "volume_tonnes": float(row.get("volume_tonnes", 0)),
                "supplier": str(row.get("supplier", "")),
                # pass cn_code directly if user already has it
                "cn_code": str(row["cn_code"]) if "cn_code" in df.columns else None,
                "category": None,
                "classification_note": None,
                "cbam_covered": None,
                "emission_factor": None,
                "embedded_emissions": None,
                "ets_price": None,
                "estimated_cbam_cost": None,
                "status": None,
            }

            output = cbam_pipeline.invoke(input_state)

            results.append({
                "product_description": output.get("product_description"),
                "country_of_origin": output.get("country_of_origin"),
                "volume_tonnes": output.get("volume_tonnes"),
                "cn_code": output.get("cn_code"),
                "category": output.get("category"),
                "cbam_covered": output.get("cbam_covered"),
                "emission_factor": output.get("emission_factor"),
                "embedded_emissions": output.get("embedded_emissions"),
                "ets_price": output.get("ets_price"),
                "estimated_cbam_cost": output.get("estimated_cbam_cost"),
                "status": output.get("status"),
                "classification_note": output.get("classification_note"),
            })

        return {
            "total_imports": len(results),
            "items": results
        }

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))