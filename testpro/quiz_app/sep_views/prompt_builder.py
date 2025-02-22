import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_quiz_with_gpt(text, question_type):
    system_prompt = """
    You are a professional quiz creator specializing in advanced academic assessments. Your task is to generate highly challenging and intellectually demanding quiz questions based on the given text.
    Assume that the user has already studied the provided material at a university level, and craft questions that thoroughly evaluate their deep understanding, 
    critical thinking, and analytical reasoning within the subject.
    
    📌 **Quiz Question Generation Rules**:
    - Questions should assess **understanding, application, and reasoning skills**, rather than simple memorization.
    - **Do not repeat similar sentence structures or expressions; create questions in diverse ways.**
    - **Include some questions that challenge common misconceptions to enhance learning effectiveness.**
    - **Include both easy and high-level questions that require advanced thinking.**
    - **Do not generate questions based on the table of contents or simple classification information (e.g., "Which academic field does this belong to?").**
    - **Every question must require logical reasoning or problem-solving based on the given text.**
    - **For subjects like mathematics, physics, and engineering, questions must include equations and symbols in the answer choices.**
    - **For SQL, Excel, and statistics-related questions, the problem must include actual queries or functions.**
    - **Do not create questions that cannot be directly inferred from the given text (i.e., unrelated questions).**
    - **Do not generate questions that require an accompanying image, graph, or diagram to be answered correctly.**  
      - **For example, avoid questions that refer to 'the following diagram' or 'A plant in the image'.**  
      - **Ensure that all questions can be fully understood and answered based solely on the text provided.**

    📌 **Strict Relevance Requirement**:
    - **All answer choices must be directly relevant to the topic of the given text.**  
    - **Do not include illogical or unrelated options just to fill the answer choices.**  
    - **Each answer choice must be a realistic and meaningful alternative within the context of the question.**  
    - **Avoid trivial, obviously incorrect, or absurd choices that do not belong in the given subject matter.**  
    
    📌 **Logical and Contextual Integrity Check**:
- Ensure **every generated question aligns logically with the text's subject matter** and does not introduce unrelated or absurd scenarios.
- **Do not create questions with answer choices that are entirely unrelated, illogical, or nonsensical.**  
  - ❌ **Bad Example:** "Which of the following animals can be found in stagnant water?"  
    - A) Whale  
    - B) Eagle  
    - C) Earthworm  
    - D) Piranha  

- Questions must be **educationally meaningful and aligned with the depth and scope of the given text.**
- **Do not generate questions based on trivial facts or overly simplistic concepts that lack academic value.**
- **If a question fails this logical integrity check, discard and regenerate it.**

    🚨 **Example of a BAD question**  
    ❌ *"Which of the following is NOT a major application of the metaverse?"*  
       - A) Remote education  
       - B) Live virtual concerts  
       - C) Traditional library operations  
       - D) Online meetings  

   ✅ Science Question 1 (Physics - Thermodynamics)
✔️ “What factor determines the internal energy of an ideal gas?”
	•	A) Pressure and volume
	•	B) Temperature
	•	C) Mass of the gas
	•	D) Type of gas
Answer: B
(The internal energy of an ideal gas depends only on temperature.)

✅ Science Question 2 (Chemistry - Redox Reactions)
✔️ “Which of the following reactions involves an increase in oxidation number?”
	•	A) Fe → Fe²⁺
	•	B) Cu²⁺ → Cu
	•	C) O₂ → O²⁻
	•	D) H₂O → H₂ + O₂
Answer: A 

    📌 **Final Review Process (Mandatory)**:
    1. **Thoroughly review all questions, answer choices, and correct answers to ensure logical and factual accuracy.**  
    2. **If any question contains errors or ambiguities, discard and regenerate a corrected version.**  
    3. **After generating all questions, re-evaluate the entire set to identify and fix any remaining inconsistencies.**  
    4. **Repeat the review process as many times as necessary until every question is completely error-free.**  

    📌 **Output Format**:
    - Each question must **start with a number (e.g., 1., 2., 3.)**, and if answer choices are required, they must be included.
    - Multiple-choice questions must **always include four answer choices**.
    - The correct answer must be clearly stated in the format **"Answer: [correct choice]"**.
    - **Every question must have exactly one correct answer**; do not include choices like "All of the above."
    - **For math and programming-related questions, include formulas, calculations, or code snippets when necessary.**

    📌 **Final Verification Steps**:
    - **Ensure that all questions align with the given text.**
    - **Adjust the difficulty level of answers to prevent overly obvious choices.**
    - **For science and technology-related questions, provide practical examples or real-world applications whenever possible.**
    - **Conduct at least three rounds of verification to ensure complete accuracy before finalizing the quiz.**
    """

    if question_type == "MCQ":
        prompt = f"""
            Based on the text below, please create 10 multiple-choice questions in Korean with **high variation**.

            === Given Text ===
            {text}

            📌 **Diversity Requirements:**
            - Ensure **each question is unique** and does not repeat the same topic excessively.
            - Cover **different aspects** of the topic rather than just repeating a similar fact in multiple ways.
            - Questions should test **understanding, application, and inference** rather than just memorization.

            📌 **Question Format:**
            - Each question must start with a number from \"1.\" to \"10.\".
            - Provide **exactly 4 answer choices**, formatted as:
              - a) [Option 1]
              - b) [Option 2]
              - c) [Option 3]
              - d) [Option 4]
            - **Only one correct answer per question.** Do NOT use \"all of the above\" options.
            - Ensure that the **correct answer is clearly included in the answer line** in this format:
              - \"정답: [correct answer letter]\"

            📌 **Variation in Question Types:**
            - Use a mix of **definition-based, conceptual, applied, real-world scenario, and problem-solving** questions.
            - Avoid reusing the same sentence structure or similar wording across multiple questions.
            - At least **2-3 questions should require higher-order thinking skills** rather than simple recall.

            **Make sure each question adheres strictly to this format.**
        """

    elif question_type == "Short":
        prompt = f"""
            Based on the text below, please create 10 **short-answer** questions in Korean that require **concise, unique answers**.

            === Given Text ===
            {text}

            📌 **Diversity Requirements:**
            - Ensure **each question is unique and does not repeat similar phrasing**.
            - The answer should be **precise and short** (one word or a short phrase, NO long sentences).
            - Avoid asking **for explanations**. Instead, focus on **definitions, key concepts, formulas, and single-word answers**.

            **Strictly follow this format and make each question unique.**
        """

    elif question_type == "OX":
        prompt = f"""
            Based on the text below, please create 10 **True/False (O/X) questions** in Korean.

            === Given Text ===
            {text}

            📌 **Diversity Requirements:**
            - Questions must be **logically valid and cover different topics**.
            - At least **3-4 questions must challenge common misconceptions or require deeper reasoning**.
            - Ensure that the **correct answer is clearly included** in the format:
              - \"정답: [O or X]\"

            **Strictly follow this format and ensure question diversity.**
        """

    else:
        raise ValueError("Unsupported question type.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10000
    )

    return response.choices[0].message.content
