from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from app.config.config import settings
from app.config.logging_config import get_logger
from app.llm_prompts.prompt_template import PROMPT_TEMPLATE
from app.llm_prompts.resume_system_instructions import RESUME_SYSTEM_PROMPT
from app.schemas.resume_chat import ResumeLLMResponse
from app.utils.general_utils import read_pdf, read_text_file

logger = get_logger(__name__)


class ResumeLLMService:
    # Initialize the model using the settings factory
    _base_llm = init_chat_model(
        model=settings.llm_model, model_provider=settings.llm_provider, temperature=0.1
    )

    # 2. Bind the structured output to the model
    # This creates a "structured" version of the LLM
    _structured_llm = _base_llm.with_structured_output(ResumeLLMResponse)

    @classmethod
    async def get_response(cls, user_query: str) -> ResumeLLMResponse:
        """Generate a response from the LLM based on the user query and resume data."""
        try:
            logger.info("Calling LLM for the user question.")
            profile = read_pdf("resume_kai.pdf")
            name = "Kai He"
            summary = read_text_file("summary_kai.txt")

            prompt_template = ChatPromptTemplate.from_messages(
                [("system", RESUME_SYSTEM_PROMPT), ("user", PROMPT_TEMPLATE)]
            )

            inputs = {
                "user_question": user_query,
                "name": name,
                "summary": summary,
                "profile": profile,
            }

            # This shows exactly what is about to be sent
            logger.info("DEBUG: Final Prompt being sent to LLM:")
            logger.info((prompt_template.format(**inputs)))
            logger.info("---------------------------")

            chain = prompt_template | cls._structured_llm

            # Invoke the chain (The variables are automatically replaced here)
            response = await chain.ainvoke(inputs)
            return response
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise e
