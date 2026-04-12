from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

# ========== 1. СПРАВОЧНИКИ ==========

class Specialty(Base):
    __tablename__ = "specialties"
    
    id              = Column(Integer, primary_key=True, index=True)
    code            = Column(String(20))
    name            = Column(String(255), nullable=False)
    department      = Column(String(255))
    qualification   = Column(String(255))
    description     = Column(String(500))
    is_active       = Column(Boolean, default=True)
    
    graduates       = relationship("Graduate", back_populates="specialty")


class GraduationYear(Base):
    __tablename__ = "graduation_years"
    
    id      = Column(Integer, primary_key=True, index=True)
    year    = Column(Integer, nullable=False, unique=True)
    
    graduates = relationship("Graduate", back_populates="graduation_year")


class Role(Base):
    __tablename__ = "roles"
    
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(50), nullable=False, unique=True)
    description     = Column(String(255))
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class AchievementType(Base):
    __tablename__ = "achievement_types"
    
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(255), nullable=False, unique=True)
    description     = Column(String(500))


class Skill(Base):
    __tablename__ = "skills"
    
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(255), nullable=False, unique=True)
    category        = Column(String(100))
    description     = Column(String(500))


class SkillLevel(Base):
    __tablename__ = "skill_levels"
    
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(50), nullable=False, unique=True)  # beginner, intermediate, advanced, expert
    value           = Column(Integer)
    description     = Column(String(255))


class JobPosition(Base):
    __tablename__ = "job_positions"
    
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(255), nullable=False)
    category        = Column(String(100))
    description     = Column(String(500))


class Employer(Base):
    __tablename__ = "employers"
    
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(255), nullable=False)
    inn             = Column(String(20))
    industry        = Column(String(255))
    website         = Column(String(500))
    phone           = Column(String(20))
    email           = Column(String(255))
    address         = Column(String(500))
    city            = Column(String(100))
    description     = Column(String(1000))
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


# ========== 2. ПОЛЬЗОВАТЕЛИ ==========

class User(Base):
    __tablename__ = "users"
    
    id                  = Column(Integer, primary_key=True, index=True)
    email               = Column(String(255), unique=True, index=True, nullable=False)
    username            = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password     = Column(String(255), nullable=False)
    full_name           = Column(String(255))
    is_active           = Column(Boolean, default=True)
    is_superuser        = Column(Boolean, default=False)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())
    last_login          = Column(DateTime(timezone=True))
    avatar_url          = Column(String(500))
    
    graduate            = relationship("Graduate", back_populates="user", uselist=False)


class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id         = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    assigned_at     = Column(DateTime(timezone=True), server_default=func.now())


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token       = Column(String(255), nullable=False, unique=True)
    expires_at  = Column(DateTime, nullable=False)
    used_at     = Column(DateTime)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())


# ========== 3. ВЫПУСКНИКИ (зависит от справочников) ==========

class Graduate(Base):
    __tablename__ = "graduates"
    
    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    first_name          = Column(String(100), nullable=False)
    last_name           = Column(String(100), nullable=False)
    middle_name         = Column(String(100))
    birth_date          = Column(Date)
    phone               = Column(String(20))
    email               = Column(String(255))
    specialty_id        = Column(Integer, ForeignKey("specialties.id"))
    graduation_year_id  = Column(Integer, ForeignKey("graduation_years.id"))
    group_name          = Column(String(50))
    diploma_number      = Column(String(50))
    diploma_date        = Column(Date)
    is_employed         = Column(Boolean, default=False)
    portfolio_url       = Column(String(500))
    linkedin_url        = Column(String(500))
    github_url          = Column(String(500))
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())
    
    user                = relationship("User", back_populates="graduate")
    specialty           = relationship("Specialty", back_populates="graduates")
    graduation_year     = relationship("GraduationYear", back_populates="graduates")
    skills              = relationship("GraduateSkill", back_populates="graduate")
    achievements        = relationship("Achievement", back_populates="graduate")
    employment_records  = relationship("EmploymentRecord", back_populates="graduate")
    feedback            = relationship("EmployerFeedback", back_populates="graduate")
    survey_responses    = relationship("SurveyResponse", back_populates="graduate")

# ========== 4. НАВЫКИ ВЫПУСКНИКОВ ==========

class GraduateSkill(Base):
    __tablename__ = "graduate_skills"
    
    graduate_id             = Column(Integer, ForeignKey("graduates.id", ondelete="CASCADE"), primary_key=True)
    skill_id                = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    level_id                = Column(Integer, ForeignKey("skill_levels.id"))
    confirmed_by_employer   = Column(Boolean, default=False)
    created_at              = Column(DateTime(timezone=True), server_default=func.now())
    
    graduate    = relationship("Graduate", back_populates="skills")
    skill       = relationship("Skill")
    level       = relationship("SkillLevel")

# ========== 5. ДОСТИЖЕНИЯ ==========

class Achievement(Base):
    __tablename__ = "achievements"
    
    id              = Column(Integer, primary_key=True, index=True)
    graduate_id     = Column(Integer, ForeignKey("graduates.id", ondelete="CASCADE"))
    type_id         = Column(Integer, ForeignKey("achievement_types.id"))
    name            = Column(String(255), nullable=False)
    issuer          = Column(String(255))
    issue_date      = Column(Date, nullable=False)
    expiry_date     = Column(Date)
    description     = Column(String(1000))
    document_url    = Column(String(500))
    verified        = Column(Boolean, default=False)
    verified_by     = Column(Integer, ForeignKey("users.id"))
    verified_at     = Column(DateTime)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    
    graduate            = relationship("Graduate", back_populates="achievements")
    achievement_type    = relationship("AchievementType")


# ========== 6. ТРУДОУСТРОЙСТВО ==========

class EmploymentRecord(Base):
    __tablename__ = "employment_records"
    
    id                  = Column(Integer, primary_key=True, index=True)
    graduate_id         = Column(Integer, ForeignKey("graduates.id", ondelete="CASCADE"))
    employer_id         = Column(Integer, ForeignKey("employers.id", ondelete="CASCADE"))
    position_id         = Column(Integer, ForeignKey("job_positions.id"))
    start_date          = Column(Date, nullable=False)
    end_date            = Column(Date)
    is_current          = Column(Boolean, default=False)
    salary              = Column(Integer)
    employment_type     = Column(String(50))
    description         = Column(String(1000))
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())
    
    graduate    = relationship("Graduate", back_populates="employment_records")
    employer    = relationship("Employer")
    position    = relationship("JobPosition")


# ========== 7. ОТЗЫВЫ ==========

class EmployerFeedback(Base):
    __tablename__ = "employer_feedback"
    
    id                  = Column(Integer, primary_key=True, index=True)
    graduate_id         = Column(Integer, ForeignKey("graduates.id", ondelete="CASCADE"))
    employer_id         = Column(Integer, ForeignKey("employers.id", ondelete="CASCADE"))
    feedback_date       = Column(Date, nullable=False)
    rating              = Column(Integer)
    strengths           = Column(String(1000))
    weaknesses          = Column(String(1000))
    recommendation      = Column(String(1000))
    would_hire_again    = Column(Boolean)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    
    graduate = relationship("Graduate", back_populates="feedback")
    employer = relationship("Employer")


# ========== 8. ОПРОСЫ ==========

class Survey(Base):
    __tablename__ = "surveys"
    
    id              = Column(Integer, primary_key=True, index=True)
    title           = Column(String(255), nullable=False)
    description     = Column(String(1000))
    start_date      = Column(Date)
    end_date        = Column(Date)
    is_active       = Column(Boolean, default=True)
    created_by      = Column(Integer, ForeignKey("users.id"))
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class SurveyQuestion(Base):
    __tablename__ = "survey_questions"
    
    id              = Column(Integer, primary_key=True, index=True)
    survey_id       = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"))
    question_text   = Column(String(1000), nullable=False)
    question_type   = Column(String(50))
    options         = Column(String(2000))  # JSON как строка для SQLite
    order           = Column(Integer)


class SurveyResponse(Base):
    __tablename__ = "survey_responses"
    
    id              = Column(Integer, primary_key=True, index=True)
    survey_id       = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"))
    graduate_id     = Column(Integer, ForeignKey("graduates.id", ondelete="CASCADE"))
    question_id     = Column(Integer, ForeignKey("survey_questions.id", ondelete="CASCADE"))
    response_text   = Column(String(2000))
    response_value  = Column(Integer)
    submitted_at    = Column(DateTime(timezone=True), server_default=func.now())
    
    graduate = relationship("Graduate", back_populates="survey_responses")