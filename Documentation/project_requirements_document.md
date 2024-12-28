# Project Requirements Document: Mapping the Climate Bioeconomy

## Project Overview

The "Mapping the Climate Bioeconomy" project is a web application designed to collate and present detailed information about companies in the bioeconomy, specifically those engaged in addressing the climate crisis. The primary objective is to create an interactive world map that accurately displays the locations and relevant details of biotech organizations working to combat climate change. The application will serve as a comprehensive resource for individuals interested in exploring the climate-focused biotech ecosystem, whether they're job seekers, industry professionals, or investors.

This project aims to create a user-friendly platform that aggregates information from multiple data sources, including CSV files, APIs, and reports, into a visually engaging and professional layout. The success of this project will be measured by the seamless integration of data, user engagement levels, and the ability to use AI to generate insightful reports, ultimately fostering a better understanding of the climate bioeconomy sector.

## In-Scope vs. Out-of-Scope

**In-Scope:**
- Development of the web application using a modern tech stack (Next.js 14, TypeScript, Tailwind CSS).
- Implementation of an interactive world map with filtering capabilities.
- Integration of data from existing spreadsheets, APIs, and other resources.
- Development of a job board displaying job openings in the climate bioeconomy space.
- A feature to generate AI-driven reports for user queries.
- Implementation of a collapsible sidebar with navigation and contact information.
- Initial implementation of user-generated content validation for submissions.
- Setting up and integrating analytics tools like Google Analytics for user interaction tracking.

**Out-of-Scope:**
- Real-time data integration is not planned for the first version but considered for future enhancements.
- Multi-language support beyond English, though planned for future iterations.
- Advanced user sign-up or credential systems beyond basic submission validations.
- Integration of additional data pipelines or AI model expansions not specified in initial planning.

## User Flow

When a new user visits the application, they will land on a minimalistic Home page that offers a brief overview of the site's purpose and tools available. From here, users can explore various sections, starting with the Climate Biotech Map. This section allows users to apply filters to view different organizations on an interactive map. Users can also contribute data by submitting their organization's information through an interactable form.

Moving forward, users have access to the Climate Biotech Jobs page, where they can filter and review current job opportunities within the sector. Another page, dedicated to Climate Biotech Regulations and Funding, provides users with the ability to generate detailed reports by inputting their requirements, leveraging AI capabilities. Throughout their journey, users can utilize the collapsible sidebar for easy navigation between sections and to access contact details.

## Core Features

- **Interactive Map:** A dynamic world map with filtering features to display biotech organizations.
- **Data Submission:** A feature allowing users to submit information about their organizations.
- **Job Board:** A section listing job openings within the climate bioeconomy.
- **Report Generation:** AI-powered reports based on user input related to regulations and funding.
- **Collapsible Sidebar:** Includes quick links and contact information for easy navigation.
- **Analytics Integration:** Understanding user behavior via Google Analytics and other tools.
- **User-Generated Content Validation:** Admin functionality for reviewing user submissions.

## Tech Stack & Tools

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, shadcn/UI, Radix UI, Lucide Icons.
- **Backend & Storage:** Supabase for handling user data and forms.
- **AI Models:** GPT-4o and Claude 3.5 Sonnet for report generation and data processing.
- **Tools:** VS Code, Bolt, V0 by Vercel, Lovable, Create XYZ for development support.

## Non-Functional Requirements

- The application should meet WCAG accessibility standards, including keyboard navigation and screen reader compatibility.
- Page components should load within two seconds to ensure smooth user experience.
- Maintain high security for financial transactions through integration with a platform like Stripe.
- Ensure data accuracy and consistency across various user interactions.

## Constraints & Assumptions

- It's assumed that all integrated APIs and data sources remain available and stable.
- The application assumes English as the primary language but plans for multilingual support.
- The use of AI models requires access to Claude AI and GPT-4o, assuming their readiness for deployment.

## Known Issues & Potential Pitfalls

- API rate limits could impact data retrieval processes; implementing caching mechanisms could mitigate this.
- Real-time data integration complexities may arise, warranting future reassessment and adaptation.
- Users might submit incorrect or poorly formatted data; incorporating validation and moderation could address this issue.
- Ensuring compliance with data privacy laws, especially concerning user-generated content, is crucial.