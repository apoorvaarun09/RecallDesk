
import os
import traceback

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

app = Flask(__name__)

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Check API configuration
if not all([
    HINDSIGHT_API_KEY,
    HINDSIGHT_BASE_URL,
    BANK_ID,
    GROQ_API_KEY
]):
    raise RuntimeError(
        "Missing configuration. Please check your .env file."
    )


# ==========================================
# 2. CONNECT TO HINDSIGHT
# ==========================================

hindsight = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY
)


# ==========================================
# 3. CONNECT TO GROQ
# ==========================================

groq_client = Groq(
    api_key=GROQ_API_KEY
)

MODEL = "openai/gpt-oss-20b"


# ==========================================
# 4. HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# 5. BACKEND HEALTH CHECK
# ==========================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "RecallDesk backend is running!"
    })


# ==========================================
# 6. CUSTOMER SUPPORT CHAT
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    customer_id = str(
        data.get("customer_id", "")
    ).strip()

    message = str(
        data.get("message", "")
    ).strip()


    # Validate customer input
    if not customer_id or not message:

        return jsonify({
            "status": "error",
            "message": "Customer ID and message are required."
        }), 400


    try:

        print("\n======================================")
        print("       NEW RECALLDESK REQUEST")
        print("======================================")

        print("Customer ID:", customer_id)
        print("Customer Message:", message)


        # ==================================
        # STEP 1: RETRIEVE PREVIOUS MEMORIES
        # ==================================

        print("\nSTEP 1: Retrieving previous memories...")

        result = hindsight.recall(
            bank_id=BANK_ID,
            query=(
                f"Customer ID: {customer_id}. "
                "Find previous customer support conversations, "
                "reported problems, troubleshooting steps, "
                "solutions attempted and their outcomes."
            )
        )

        memories = [
            memory.text
            for memory in result.results
        ]

        print("Retrieved memories:", len(memories))

        if memories:

            memory_context = "\n\n".join(memories)

        else:

            memory_context = (
                "No previous memories found for this customer."
            )

        print("STEP 1 SUCCESS")


        # ==================================
        # STEP 2: PREPARE AI INSTRUCTIONS
        # ==================================

        print("\nSTEP 2: Preparing AI instructions...")

        system_prompt = """
        You are RecallDesk, an intelligent AI customer support
        agent with persistent memory.

        Your main goal is to provide continuous customer support
        by remembering previous interactions.

        FOLLOW THESE RULES:

        1. Understand the customer's current problem.

        2. Carefully review the previous customer memories.

        3. Identify previous problems and troubleshooting
           steps already attempted.

        4. When relevant memories exist, briefly acknowledge
           them naturally in your response.

        5. For example:
           "I remember that you previously reported Wi-Fi
           disconnections and tried restarting your router."

        6. Never claim to remember information that is not
           present in the retrieved memories.

        7. Never assume that a suggested solution was attempted.

        8. If the customer confirms a solution failed,
           do not recommend the same solution again unless
           there is a clear reason.

        9. If the outcome of a previous suggestion is unknown,
           ask the customer before assuming it failed.

        10. Suggest sensible new troubleshooting steps.

        11. Ask relevant questions when more information
            is needed.

        12. Give simple, practical and step-by-step instructions.

        13. Be friendly, polite and concise.

        14. Never invent customer history.

        IMPORTANT:
        Always prioritize relevant previous memories when
        responding to returning customers.
        """


        # ==================================
        # STEP 3: PREPARE CUSTOMER CONTEXT
        # ==================================

        print("\nSTEP 3: Preparing customer context...")

        user_prompt = f"""
        CUSTOMER ID:
        {customer_id}

        PREVIOUS CUSTOMER MEMORIES:
        {memory_context}

        CURRENT CUSTOMER MESSAGE:
        {message}

        INSTRUCTIONS:

        Read the previous memories carefully.

        If relevant previous conversations exist, acknowledge
        the important details naturally.

        Identify which troubleshooting steps were attempted
        and whether they worked or failed.

        Do not repeat unsuccessful solutions.

        Respond to the customer's current problem with
        helpful next steps.
        """

        print("STEP 3 SUCCESS")


        # ==================================
        # STEP 4: GENERATE AI RESPONSE
        # ==================================

        print("\nSTEP 4: Generating AI response...")

        completion = groq_client.chat.completions.create(

            model=MODEL,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ],

            temperature=0.5
        )

        reply = completion.choices[0].message.content

        if not reply:

            raise RuntimeError(
                "Groq returned an empty response."
            )

        print("STEP 4 SUCCESS")

        print("\nAI RESPONSE:")
        print(reply)


        # ==================================
        # STEP 5: SAVE CONVERSATION
        # ==================================

        print("\nSTEP 5: Saving conversation to Hindsight...")

        hindsight.retain(

            bank_id=BANK_ID,

            content=f"""
            Customer ID: {customer_id}

            Customer message:
            {message}

            Assistant response:
            {reply}

            Important:
            This conversation has been recorded.

            Do not assume that a suggested troubleshooting
            step was attempted or successful unless the
            customer confirms its outcome.
            """,

            context="RecallDesk customer support conversation"
        )

        print("STEP 5 SUCCESS")
        print("Conversation saved successfully!")


        # ==================================
        # STEP 6: RETURN RESPONSE TO FRONTEND
        # ==================================

        print("\nSTEP 6: Sending response to frontend...")

        return jsonify({

            "status": "success",

            "customer_id": customer_id,

            "reply": reply,

            "memory_used": len(memories) > 0,

            "memories": memories

        })


    # ==================================
    # ERROR HANDLING
    # ==================================

    except Exception as e:

        print("\n======================================")
        print("           RECALLDESK ERROR")
        print("======================================")

        print("Error Type:", type(e).__name__)
        print("Error Message:", str(e))

        traceback.print_exc()

        print("======================================")

        return jsonify({

            "status": "error",

            "message": "Backend error. Check Flask terminal."

        }), 500


# ==========================================
# 7. RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False,
        threaded=False
    )
