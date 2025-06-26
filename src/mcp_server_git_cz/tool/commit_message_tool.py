import os
from collections.abc import AsyncIterator

import mcp.types as types
from openai import AsyncOpenAI
from groq import AsyncGroq

from .git_utils import get_git_diff


class CommitMessageTool:
    def __init__(self, llm_provider: str):
        self.llm_provider = llm_provider
        if self.llm_provider == "groq":
            self.client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
            self.model = "llama3-8b-8192"
        else:
            self.client = AsyncOpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
            self.model = "deepseek-chat"

    async def call(self, name: str, arguments: dict) -> AsyncIterator[types.TextContent]:
        diff = get_git_diff()
        if diff.startswith("Error:"):
            yield types.TextContent(type="text", text=diff)
            return

        if not diff.strip():
            yield types.TextContent(type="text", text="feat: No changes detected")
            return

        system_prompt = (
            "You are a helpful assistant that generates commit messages in the "
            "Conventional Commits format."
        )

        user_prompt = f'''# Git diff

@{{git_diff}}

------

Generate an English commit message that meets the friendly requirements of commitizen from git difft:

# Examples

```
feat(home): add ad
- Introduced the @ctrl/react-adsense package to enable Google AdSense integration in the application.
- Updated package.json and pnpm-lock.yaml to include the new dependency.
- Added the Adsense component in page.tsx to display ads, enhancing monetization opportunities.
- Included a script tag in layout.tsx for loading the AdSense script asynchronously.


These changes improve the application's revenue potential while maintaining a clean and organized codebase.
```

------

```
refactor(cmpts)!: rename input form
- Renamed `InputForm.tsx` to `input-form.tsx` to follow consistent naming conventions.
- Updated the import path in `app/page.tsx` to reflect the renamed file.

BREAKING CHANGE: This change renames `InputForm.tsx` to `input-form.tsx`, which will require updates to any imports referencing the old file name.
```

------

```
feat(api): refactor client and improve hexagram
- Replaced `openai` import with `createOpenAI` to allow for customizable settings.
- Added support for custom OpenAI API base URL configuration.
- Enhanced hexagram generation logic:
  - Improved randomness simulation for hexagram line generation.
  - Refactored `determineLineType` for better readability and error handling.
  - Optimized transformation logic for moving lines.
  - Standardized logging format for debug messages.
  - Updated hexagram data structure for consistency and clarity.
  - Fixed typos and logical errors in several hexagram mappings.

These changes improve code readability, maintainability, and debugging efficiency.
```

# Overview

Each commit message must follow a structured format and remain succinct and clear. The message consists of three parts—a header (all lowercase), a body (capitalized at the beginning of every line), and a footer. The header is mandatory and must conform to the following format: `type(scope): subject`. The body must begin with one blank line after the header and every line should be capitalized. The footer can contain breaking changes and issue references.

## Header

The header is the most important part of the commit message. It should be a single line that summarizes the change. The type must be one of the following: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert. The scope is optional and should be a noun describing the area of the codebase that the change affects. The subject should be a short, imperative-tense description of the change.

## Body

The body is optional, but it is highly recommended. It should provide more context about the change, including the motivation and the approach. Use the imperative, present tense: "change" not "changed" nor "changes". The body should include the motivation for the change and contrast this with previous behavior. Capitalized at the beginning.

## Footer

The footer should contain any information about Breaking Changes and is also the place to reference GitHub issues that this commit closes.
Breaking Changes should start with the word BREAKING CHANGE: with a space or two newlines. The rest of the commit message is then used for this. Capitalized at the beginning.

Diff:
```
{diff}
```
'''

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True
        )
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield types.TextContent(type="text", text=content)