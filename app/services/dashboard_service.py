from sqlalchemy.orm import Session, joinedload
from app.models.center import Center
from app.models.mosque import Mosque
from app.models.study_circle import StudyCircle


def get_dashboard_data(db: Session):
    centers = db.query(Center).options(
        joinedload(Center.mosques).joinedload(Mosque.study_circles).joinedload(StudyCircle.teacher),
        joinedload(Center.mosques).joinedload(Mosque.study_circles).joinedload(StudyCircle.students)
    ).all()

    dashboard = []
    for center in centers:
        center_data = {
            "center_id": center.id,
            "center_name": center.name,
            "total_mosques": len(center.mosques),
            "mosques": []
        }
        total_study_circles = 0
        for mosque in center.mosques:
            mosque_data = {
                "mosque_id": mosque.id,
                "mosque_name": mosque.name,
                "total_study_circles": len(mosque.study_circles),
                "study_circles": []
            }
            total_study_circles += len(mosque.study_circles)
            for circle in mosque.study_circles:
                teacher_name = circle.teacher.full_name if circle.teacher else None
                mosque_data["study_circles"].append({
                    "study_circle_id": circle.id,
                    "study_circle_name": circle.name,
                    "teacher_name": teacher_name,
                    "status": circle.status.value if circle.status else None,
                    "type": circle.type.value if circle.type else None,
                    "max_capacity": circle.max_capacity,
                    "total_students": len(circle.students)
                })
            center_data["mosques"].append(mosque_data)
        center_data["total_study_circles"] = total_study_circles
        dashboard.append(center_data)
    return dashboard
