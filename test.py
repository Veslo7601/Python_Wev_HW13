@router.get("/", response_model=List[NoteResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    notes = await repository_notes.get_notes(skip, limit, current_user, db)
    return notes
