# Microsoft IQ Intelligence Layer Architecture

## CareerVerse AI implements a 3-tier Intelligence Layer:

### Layer 1: Knowledge Extraction (Foundry IQ Pattern)
Resume PDF → Text Extraction → Entity Recognition → Knowledge Graph
↓ ↓ ↓
Raw Text Skills, Projects, Connected Data
Certs, Education Points

text

**Implementation:**
- extract_text() - PyPDF2 text extraction
- extract_skills() - Pattern matching against 50+ skills
- extract_projects() - NLP-based project detection
- extract_certifications() - Certification pattern recognition
- extract_education() - Education entity extraction

### Layer 2: Semantic Understanding (Work IQ Pattern)
Knowledge Graph → Context Building → Relationship Mapping
↓ ↓
Career Context Skill-Project-Cert
Relationships

text

**Implementation:**
- Skill-to-role mapping matrix
- Project-to-experience correlation
- Certification-to-expertise weighting
- Career trajectory analysis

### Layer 3: Career Reasoning (Fabric IQ Pattern)
Relationships → Role Inference → Gap Analysis → Decision Engine
↓ ↓ ↓
Detected Role Missing Skills Personalized
Recommendations

text

**Implementation:**
- detect_role() - Multi-factor role scoring
- analyze_skill_gap() - Industry requirement comparison
- generate_quests() - Personalized learning missions
- generate_story() - Narrative engine
- generate_mentor_advice() - AI career counseling
- generate_roadmap() - Structured learning path

### Output Intelligence:
- Role Detection with confidence scoring
- Skill gap analysis against industry standards
- XP calculation based on real achievements
- Dynamic quest generation from missing skills
- Personalized story narratives from actual data
- Mentor guidance tailored to career stage
- Learning roadmap with milestones

### Key Innovation:
CareerVerse AI's intelligence layer:
1. Adapts to any resume - No predefined roles or skills
2. Reasons over real data - Every output is derived from actual resume content
3. Creates personalized experiences - Each user gets unique badges, quests, and stories
4. Learns industry patterns - Skill gap analysis uses current market requirements
