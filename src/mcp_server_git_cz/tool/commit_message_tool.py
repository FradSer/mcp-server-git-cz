import os
from collections.abc import AsyncIterator

import mcp.types as types
from openai import AsyncOpenAI

from .git_utils import get_git_diff


class CommitMessageTool:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

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
        user_prompt = (
            "# Git diff\n\n @{{git_diff}}\n\n------\n\nGenerate an English commit message that meets the friendly requirements of commitizen from git difft:\n\n# Examples\n\n``` \nfeat(home): add ad\n- Introduced the @ctrl/react-adsense package to enable Google AdSense integration in the application.\n- Updated package.json and pnpm-lock.yaml to include the new dependency.\n- Added the Adsense component in page.tsx to display ads, enhancing monetization opportunities.\n- Included a script tag in layout.tsx for loading the AdSense script asynchronously.\n\n\nThese changes improve the application's revenue potential while maintaining a clean and organized codebase.\n```\n\n------\n\n```\nrefactor(cmpts)!: rename input form\n- Renamed `InputForm.tsx` to `input-form.tsx` to follow consistent naming conventions.\n- Updated the import path in `app/page.tsx` to reflect the renamed file.\n\nBREAKING CHANGE: This change renames `InputForm.tsx` to `input-form.tsx`, which will require updates to any imports referencing the old file name.\n```\n\n------\n\n```\nfeat(api): refactor client and improve hexagram\n- Replaced `openai` import with `createOpenAI` to allow for customizable settings.\n- Added support for custom OpenAI API base URL configuration.\n- Enhanced hexagram generation logic:\n  - Improved randomness simulation for hexagram line generation.\n  - Refactored `determineLineType` for better readability and error handling.\n  - Optimized transformation logic for moving lines.\n  - Standardized logging format for debug messages.\n- Updated hexagram data structure for consistency and clarity.\n- Fixed typos and logical errors in several hexagram mappings.\n\nThese changes improve code readability, maintainability, and debugging efficiency.\n```\n\n# Overview\n\nEach commit message must follow a structured format and remain succinct and clear. The message consists of three parts—a header (all lowercase), a body (capitalized at the beginning of every line), and a footer (capitalized at the beginning.)—and every line should be under 100 characters. The commit title (i.e. the header) must be entirely lowercase and limited to 50 characters.\n\n# Commit Message Structure\n\nEach commit message consists of a header, a body and a footer. The header has a special format that includes a type, a scope and a subject:\n\n\n```\n<type>(<scope>): <subject>\n<BLANK LINE>\n<body>\n<BLANK LINE>\n<footer>\n```\n\n- Header: Mandatory. It follows the format `<type>(<scope>): <subject>`. The scope is optional.\n- Body: Explains the reason for the change and contrasts it with previous behavior.\n- Footer: Contains references to issues and information about breaking changes.\n\n# General Rules\n- Title Requirements:\n  - Use all lowercase letters.\n  - Keep it under 50 characters.\n- Line Length:\n  - No single line should exceed 100 characters.\n- Footer Inclusion:\n  - Every commit must include a footer. Use it to list GitHub issue references or describe breaking changes.\n\n## Type\n\nMust be one of the following:\n- feat: A new feature\n- fix: A bug fix\n- docs: Documentation only changes\n- style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)\n- refactor: A code change that neither fixes a bug nor adds a feature\n- perf: A code change that improves performance\n- test: Adding missing or correcting existing tests\n- chore: Changes to the build process or auxiliary tools and libraries such as documentation generation\n\n## Scope\n\nThe scope could be anything specifying place of the commit change. For example $location, $browser, $compile, $rootScope, ngHref, ngClick, ngView, etc...\nYou can use * when the change affects more than a single scope.\n\n## Subject\n\nThe subject contains succinct description of the change:\nuse the imperative, present tense: "change" not "changed" nor "changes"\ndon't capitalize first letter\nno dot (.) at the end\n\n## Body\n\nJust as in the subject, use the imperative, present tense: "change" not "changed" nor "changes". The body should include the motivation for the change and contrast this with previous behavior. Capitalized at the beginning.\n\n## Footer\n\nThe footer should contain any information about Breaking Changes and is also the place to reference GitHub issues that this commit closes.\nBreaking Changes should start with the word BREAKING CHANGE: with a space or two newlines. The rest of the commit message is then used for this. Capitalized at the beginning."
            f"Diff:\n```\n{diff}\n```"
        )

        response = await self.client.chat.completions.create(
            model="deepseek-chat",
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