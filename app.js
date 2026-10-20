/**
 * NNDEPSPORT OFFICIAL SPORTS PLATFORM - APPLICATION CONTROLLER
 * Fusion of T-Bank Modern Minimalism + Superliga RFS Futsal Architecture
 */

document.addEventListener('DOMContentLoaded', () => {
  const data = window.SITE_DATA || {
    team_name: 'Доза Агро',
    city: 'Нижний Новгород',
    players: [],
    matches: [],
    standings: []
  };

  // State
  let currentPosition = 'all';
  let currentViewMode = 'cards'; // 'cards' | 'table'
  let searchVal = '';

  // DOM Elements
  const squadGroupedOutput = document.getElementById('squadGroupedOutput');
  const squadSearchField = document.getElementById('squadSearchField');
  const positionFilters = document.getElementById('positionFilters');
  const btnModeCards = document.getElementById('btnModeCards');
  const btnModeTable = document.getElementById('btnModeTable');

  const calendarMatchList = document.getElementById('calendarMatchList');
  const leagueStandingsBody = document.getElementById('leagueStandingsBody');
  const tabButtons = document.querySelectorAll('.t-tab-item');
  const tabPanels = document.querySelectorAll('.tab-view-panel');

  const playerModal = document.getElementById('playerModal');
  const playerModalBody = document.getElementById('playerModalBody');
  const btnClosePlayerModal = document.getElementById('btnClosePlayerModal');
  const btnDownloadIcs = document.getElementById('btnDownloadIcs');

  // Photo Lightbox Elements
  const photoLightbox = document.getElementById('photoLightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const lightboxSubtext = document.getElementById('lightboxSubtext');
  const lightboxOpenOriginal = document.getElementById('lightboxOpenOriginal');
  const btnCloseLightbox = document.getElementById('btnCloseLightbox');
  const btnOpenTeamPhoto = document.getElementById('btnOpenTeamPhoto');
  const clubShieldBtn = document.getElementById('clubShieldBtn');
  const leaderItemPavlyuk = document.getElementById('leaderItemPavlyuk');
  const leaderItemBalashov = document.getElementById('leaderItemBalashov');

  // Photo Lightbox Controller
  function getHighResPhoto(url) {
    if (!url) return '';
    return url.replace('/small/', '/normal/');
  }

  function openPhotoLightbox(imgUrl, titleText, subText) {
    if (!photoLightbox || !imgUrl) return;
    lightboxImg.src = imgUrl;
    lightboxImg.alt = titleText || 'Фотография';
    if (lightboxTitle) lightboxTitle.textContent = titleText || 'Фотография';
    if (lightboxSubtext) lightboxSubtext.textContent = subText || 'Оригинальное качество • Наградион ЕИС';
    if (lightboxOpenOriginal) lightboxOpenOriginal.href = imgUrl;
    photoLightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closePhotoLightbox() {
    if (!photoLightbox) return;
    photoLightbox.classList.remove('active');
    if (!playerModal || !playerModal.classList.contains('active')) {
      document.body.style.overflow = '';
    }
  }

  if (btnCloseLightbox) {
    btnCloseLightbox.addEventListener('click', closePhotoLightbox);
  }

  if (photoLightbox) {
    photoLightbox.addEventListener('click', (e) => {
      if (e.target === photoLightbox || e.target.id === 'lightboxWrap') {
        closePhotoLightbox();
      }
    });
  }

  if (btnOpenTeamPhoto) {
    btnOpenTeamPhoto.addEventListener('click', () => {
      openPhotoLightbox(
        data.team_photo || 'https://img.nagradion.ru/images/big/teams/teamb61fad2fc6202861fc9a3b03ef516825.jpg',
        'МФК «Доза Агро» • Общекомандное фото',
        'Заявочный состав на Первую лигу 2026/2027 (18 игроков, 2 руководителя)'
      );
    });
  }

  if (clubShieldBtn) {
    clubShieldBtn.addEventListener('click', () => {
      openPhotoLightbox(
        data.team_logo || 'https://img.nagradion.ru/images/bf300x500/shields/4b5baf713d124abd.png',
        'МФК «Доза Агро» • Официальная клубная эмблема',
        'Нижний Новгород • Чемпионат города по мини-футболу'
      );
    });
  }

  if (leaderItemPavlyuk) {
    leaderItemPavlyuk.addEventListener('click', () => {
      openPhotoLightbox(
        'https://img.nagradion.ru/images/normal/m/playerac2d91dcabaf0009494f10c994c5ffff.jpg',
        'Павлюк Александр • Руководитель команды',
        'МФК «Доза Агро» • Наградион ЕИС'
      );
    });
  }

  if (leaderItemBalashov) {
    leaderItemBalashov.addEventListener('click', () => {
      openPhotoLightbox(
        'https://img.nagradion.ru/images/normal/m/player0ed34af96bbb2dcc08bc7340b192dc53.jpg',
        'Балашов Максим • Тренер / Капитан',
        'МФК «Доза Агро» • Наградион ЕИС'
      );
    });
  }

  // Permanently clean light theme
  document.documentElement.setAttribute('data-theme', 'light');
  document.body.setAttribute('data-theme', 'light');

  // =========================================================================
  // 2. SQUAD RENDERING & FILTERS (Superliga Structure + T-Bank Minimalist Cards)
  // =========================================================================
  function getPositionBadgeClass(pos) {
    switch (pos) {
      case 'Вратарь': return 'pos-gk';
      case 'Защитник': return 'pos-def';
      case 'Нападающий': return 'pos-fwd';
      case 'Универсал': return 'pos-uni';
      default: return 'pos-pol';
    }
  }

  function getInitials(name) {
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
  }

  function renderSquad() {
    squadGroupedOutput.innerHTML = '';

    const query = searchVal.trim().toLowerCase();
    const filtered = data.players.filter(p => {
      const matchPos = (currentPosition === 'all') || (p.position === currentPosition);
      const matchSearch = !query ||
        p.name.toLowerCase().includes(query) ||
        (p.number && p.number.toString().includes(query));
      return matchPos && matchSearch;
    });

    if (filtered.length === 0) {
      squadGroupedOutput.innerHTML = `
        <div style="text-align: center; padding: 48px 20px; color: var(--text-muted); background: var(--bg-card); border: 1px solid var(--border-card); border-radius: var(--radius-md);">
          <div style="font-size: 15px; font-weight: 700; color: var(--text-title); margin-bottom: 4px;">Игроков не найдено</div>
          <div style="font-size: 13px;">По запросу «${searchVal}» ничего не найдено в заявке</div>
        </div>
      `;
      return;
    }

    const groups = [
      { key: 'Вратарь', title: 'Вратари' },
      { key: 'Защитник', title: 'Защитники' },
      { key: 'Универсал', title: 'Универсалы' },
      { key: 'Нападающий', title: 'Нападающие' },
      { key: 'Полевой', title: 'Полевые игроки' }
    ];

    groups.forEach(grp => {
      const grpPlayers = filtered.filter(p => p.position === grp.key);
      if (grpPlayers.length === 0) return;

      const groupWrapper = document.createElement('div');
      groupWrapper.className = 'squad-group-section';

      groupWrapper.innerHTML = `
        <div class="group-header-banner">
          <div class="group-title-tag">
            <span>${grp.title}</span>
          </div>
          <span class="group-count-badge">${grpPlayers.length}</span>
        </div>
      `;

      if (currentViewMode === 'table') {
        // Superliga RFS Clean Table Structure
        const tableCard = document.createElement('div');
        tableCard.className = 'squad-table-card';
        const isGkGroup = grp.key === 'Вратарь';

        let tHtml = `
          <table class="superliga-roster-table ${isGkGroup ? 'gk-roster-table' : ''}">
            <thead>
              <tr>
                <th style="width: 44px;">#</th>
                <th>Игрок</th>
                <th style="width: 80px;">Возраст</th>
                <th style="width: 100px;">Амплуа</th>
                <th style="width: 60px; text-align: center;" title="Сыграно матчей">Игры</th>
                ${isGkGroup ? `
                  <th style="width: 70px; text-align: center;" title="Пропущено мячей">Проп.</th>
                  <th style="width: 75px; text-align: center;" title="Матчи на ноль («сухие»)">На ноль</th>
                  <th style="width: 75px; text-align: center;" title="Пропущено с 6-метровых (пенальти)">6м (пен)</th>
                  <th style="width: 75px; text-align: center;" title="Пропущено с 10-метровых (дабл-пенальти)">10м (дабл)</th>
                ` : `
                  <th style="width: 60px; text-align: center;">Голы</th>
                  <th style="width: 60px; text-align: center;">Пасы</th>
                `}
                <th style="width: 70px; text-align: right;">Профиль</th>
              </tr>
            </thead>
            <tbody>
        `;

        grpPlayers.forEach(p => {
          const initials = getInitials(p.name);
          const hasPhoto = p.photo && p.photo.trim().length > 0;
          const numStr = p.number && p.number !== '—' ? p.number : '—';
          const ageStr = p.age ? `${p.age}` : '—';

          let statsCells = '';
          if (isGkGroup) {
            statsCells = `
              <td style="text-align: center; font-family: var(--font-display); font-weight: 600;">${p.matches_played ?? 1}</td>
              <td style="text-align: center; font-family: var(--font-display); font-weight: 800; color: var(--accent-red);">${p.goals_conceded ?? 0}</td>
              <td style="text-align: center; font-family: var(--font-display); font-weight: 800; color: var(--accent-green);">${p.clean_sheets ?? 0}</td>
              <td style="text-align: center; font-family: var(--font-display); font-weight: 700; color: var(--text-title);">${p.penalty_6m_conceded ?? 0}</td>
              <td style="text-align: center; font-family: var(--font-display); font-weight: 700; color: var(--text-title);">${p.penalty_10m_conceded ?? 0}</td>
            `;
          } else {
            statsCells = `
              <td style="text-align: center; font-family: var(--font-display); font-weight: 600;">${p.matches_played ?? 1}</td>
              <td style="text-align: center; font-family: var(--font-display); font-weight: 800; color: var(--accent-green);">${p.goals ?? 0}</td>
              <td style="text-align: center; font-family: var(--font-display); font-weight: 700; color: var(--brand-primary);">${p.assists ?? 0}</td>
            `;
          }

          tHtml += `
            <tr data-id="${p.id}">
              <td style="font-family: var(--font-display); font-weight: 800; color: var(--brand-primary);">${numStr}</td>
              <td>
                <div class="table-person-cell">
                  ${hasPhoto
              ? `<img src="${p.photo}" class="table-person-thumb" alt="${p.name}" onerror="this.style.display='none'">`
              : `<div class="table-person-thumb" style="display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:var(--brand-primary);">${initials}</div>`
            }
                  <strong style="color: var(--text-title);">${p.name}</strong>
                </div>
              </td>
              <td>${ageStr}</td>
              <td><span class="position-badge ${getPositionBadgeClass(p.position)}">${p.position}</span></td>
              ${statsCells}
              <td style="text-align: right;">
                <button class="t-btn t-btn-secondary" style="height: 28px; padding: 0 10px; font-size: 11px;">Досье</button>
              </td>
            </tr>
          `;
        });

        tHtml += `</tbody></table>`;
        tableCard.innerHTML = tHtml;

        tableCard.querySelectorAll('tbody tr').forEach(tr => {
          const pid = tr.getAttribute('data-id');
          const pObj = data.players.find(x => x.id === pid);
          if (pObj) {
            tr.addEventListener('click', () => openModal(pObj));

            const thumb = tr.querySelector('.table-person-thumb');
            if (thumb && pObj.photo) {
              thumb.setAttribute('title', `Нажмите для увеличения фото: ${pObj.name}`);
              thumb.addEventListener('click', (e) => {
                e.stopPropagation();
                openPhotoLightbox(
                  getHighResPhoto(pObj.photo),
                  `${pObj.name} • ${pObj.position} ${pObj.number && pObj.number !== '—' ? '№' + pObj.number : ''}`,
                  `${data.team_name} (Нижний Новгород) • Наградион ID ${pObj.id}`
                );
              });
            }
          }
        });

        groupWrapper.appendChild(tableCard);
      } else {
        // T-Bank Style 20px Rounded Cards
        const cardsGrid = document.createElement('div');
        cardsGrid.className = 'squad-grid-cards';

        grpPlayers.forEach(p => {
          const card = document.createElement('div');
          card.className = 't-player-card';
          card.setAttribute('data-id', p.id);

          const initials = getInitials(p.name);
          const hasPhoto = p.photo && p.photo.trim().length > 0;
          const numStr = p.number && p.number !== '—' ? p.number : '—';
          const ageStr = p.age ? `${p.age} лет` : 'Возраст не указан';
          const isGk = p.position === 'Вратарь';

          const miniStatsHtml = isGk ? `
            <div class="player-stats-mini-row gk-stats-row">
              <span class="mini-stat-item" title="Пропущено голов">Проп: <strong style="color: var(--accent-red);">${p.goals_conceded ?? 0}</strong></span>
              <span class="mini-stat-sep">•</span>
              <span class="mini-stat-item" title="Матчи на ноль («сухие»)">На ноль: <strong style="color: var(--accent-green);">${p.clean_sheets ?? 0}</strong></span>
              <span class="mini-stat-sep">•</span>
              <span class="mini-stat-item" title="Пропущено с 6м (пен) / 10м (дабл)">6м/10м: <strong>${p.penalty_6m_conceded ?? 0}/${p.penalty_10m_conceded ?? 0}</strong></span>
            </div>
          ` : `
            <div class="player-stats-mini-row field-stats-row">
              <span class="mini-stat-item" title="Сыграно матчей">Игры: <strong>${p.matches_played ?? 1}</strong></span>
              <span class="mini-stat-sep">•</span>
              <span class="mini-stat-item" title="Забито голов">Голы: <strong style="color: var(--accent-green);">${p.goals ?? 0}</strong></span>
              <span class="mini-stat-sep">•</span>
              <span class="mini-stat-item" title="Голевые передачи">Пасы: <strong>${p.assists ?? 0}</strong></span>
            </div>
          `;

          card.innerHTML = `
            <div class="player-portrait-box">
              ${hasPhoto
              ? `<img src="${p.photo}" class="player-portrait-img" alt="${p.name}" loading="lazy" onerror="this.outerHTML='<div class=\\'player-portrait-initials\\'>${initials}</div>'">`
              : `<div class="player-portrait-initials">${initials}</div>`
            }
            </div>
            <div class="player-card-details">
              <div class="player-name-line">
                <span class="player-full-name" title="${p.name}">${p.name}</span>
                <span class="player-jersey-number">${numStr}</span>
              </div>
              <div class="player-meta-line">
                <span class="position-badge ${getPositionBadgeClass(p.position)}">${p.position}</span>
                <span class="player-age-text">${ageStr}</span>
              </div>
              ${miniStatsHtml}
            </div>
          `;

          card.addEventListener('click', () => openModal(p));

          const portraitBox = card.querySelector('.player-portrait-box');
          if (portraitBox) {
            portraitBox.setAttribute('title', hasPhoto ? `Нажмите, чтобы увеличить фото: ${p.name}` : p.name);
            portraitBox.addEventListener('click', (e) => {
              if (hasPhoto) {
                e.stopPropagation();
                openPhotoLightbox(
                  getHighResPhoto(p.photo),
                  `${p.name} • ${p.position} ${numStr !== '—' ? '№' + numStr : ''}`,
                  `${data.team_name} (Нижний Новгород) • Наградион ID ${p.id}`
                );
              }
            });
          }

          cardsGrid.appendChild(card);
        });

        groupWrapper.appendChild(cardsGrid);
      }

      squadGroupedOutput.appendChild(groupWrapper);
    });
  }

  // Search input handler
  if (squadSearchField) {
    squadSearchField.addEventListener('input', (e) => {
      searchVal = e.target.value;
      renderSquad();
    });
  }

  // Position filter pills
  if (positionFilters) {
    positionFilters.addEventListener('click', (e) => {
      const btn = e.target.closest('.t-filter-pill');
      if (!btn) return;
      positionFilters.querySelectorAll('.t-filter-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentPosition = btn.getAttribute('data-pos');
      renderSquad();
    });
  }

  // View mode switcher (Cards / Table)
  btnModeCards.addEventListener('click', () => {
    currentViewMode = 'cards';
    btnModeCards.classList.add('active');
    btnModeTable.classList.remove('active');
    renderSquad();
  });

  btnModeTable.addEventListener('click', () => {
    currentViewMode = 'table';
    btnModeTable.classList.add('active');
    btnModeCards.classList.remove('active');
    renderSquad();
  });

  // =========================================================================
  // 3. CALENDAR & MATCHES (Superliga Schedule Flow)
  // =========================================================================
  function renderCalendar() {
    calendarMatchList.innerHTML = '';

    data.matches.forEach(m => {
      const card = document.createElement('div');
      const isCompleted = m.status === 'completed';
      const isNext = m.status === 'next';
      card.className = `rfs-match-card ${isNext ? 'is-spotlight' : ''} ${isCompleted ? 'is-completed' : ''}`;

      const isDozAHome = m.team1.includes('Доза Агро');
      const isDozAAway = m.team2.includes('Доза Агро');

      let statusBadgeText = '1-й круг';
      let statusBadgeColor = 'var(--text-muted)';
      if (isCompleted) {
        statusBadgeText = 'Завершен';
        statusBadgeColor = 'var(--accent-green)';
      } else if (isNext) {
        statusBadgeText = 'Ближайший';
        statusBadgeColor = 'var(--accent-amber)';
      }

      card.innerHTML = `
        <div class="match-header-row">
          <span class="tour-indicator">${m.tour}-й тур • Первая лига</span>
          <span class="match-date-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            ${m.date}
          </span>
        </div>

        <div class="match-teams-layout">
          <div class="team-block home">
            <div>
              <div class="team-display-name ${isDozAHome ? 'my-club' : ''}">${m.team1}</div>
              <div style="font-size: 11px; color: var(--text-muted);">Хозяева площадки</div>
            </div>
            <div class="team-emblem-circle">${m.team1.slice(0, 2).toUpperCase()}</div>
          </div>

          <div class="match-score-pill">
            <div class="score-value-bold" style="${isCompleted ? 'border-color: var(--accent-green);' : ''}">${m.score}</div>
            <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: ${statusBadgeColor};">
              ${statusBadgeText}
            </div>
          </div>

          <div class="team-block away">
            <div class="team-emblem-circle">${m.team2.slice(0, 2).toUpperCase()}</div>
            <div>
              <div class="team-display-name ${isDozAAway ? 'my-club' : ''}">${m.team2}</div>
              <div style="font-size: 11px; color: var(--text-muted);">Гости</div>
            </div>
          </div>
        </div>

        ${m.note ? `
          <div style="margin: 8px 0 12px; padding: 8px 12px; background: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-xs); font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 8px;">
            <span>${m.note}</span>
          </div>
        ` : ''}

        <div class="match-footer-row">
          <div class="match-location-link">
            <strong>${m.venue}</strong>
            <a href="https://yandex.ru/maps/?text=${encodeURIComponent(m.venue + ' Нижний Новгород')}" target="_blank" rel="noopener">На карте</a>
          </div>

          <div style="display: flex; gap: 8px;">
            <a href="${data.tournament_url}/match/${m.match_id}" target="_blank" rel="noopener" class="t-btn ${isCompleted ? 't-btn-primary' : 't-btn-secondary'}" style="height: 32px; padding: 0 12px; font-size: 12px;">
              ${isCompleted ? 'Протокол матча' : 'Превью матча'}
            </a>
            ${isNext ? `
              <button class="t-btn t-btn-primary" style="height: 32px; padding: 0 12px; font-size: 12px;" onclick="window.downloadICS('${m.team1}', '${m.team2}', '${m.venue}')">
                + В календарь
              </button>
            ` : ''}
          </div>
        </div>
      `;

      calendarMatchList.appendChild(card);
    });
  }

  // =========================================================================
  // 4. STANDINGS TABLE (Superliga Structure)
  // =========================================================================
  function renderStandings() {
    leagueStandingsBody.innerHTML = '';

    data.standings.forEach(row => {
      const tr = document.createElement('tr');
      const isMyTeam = row.team === 'Доза Агро';
      if (isMyTeam) tr.className = 'highlight-row';

      const formHtml = row.form.map(f => {
        const cls = f === 'W' ? 'win' : (f === 'D' ? 'draw' : 'loss');
        const letter = f === 'W' ? 'В' : (f === 'D' ? 'Н' : 'П');
        return `<span class="form-pill-tag ${cls}">${letter}</span>`;
      }).join('');

      tr.innerHTML = `
        <td><span style="font-weight: 800; color: var(--text-muted);">${row.pos}</span></td>
        <td class="col-club-left">
          <div class="club-cell-content" style="display: flex; align-items: center; gap: 10px;">
            ${row.shield ? `
              <img src="${row.shield}" alt="${row.team}" style="width: 26px; height: 26px; object-fit: contain; border-radius: 4px; background: #ffffff; padding: 1px; border: 1px solid var(--border-subtle); flex-shrink: 0;" onerror="this.style.display='none'">
            ` : `
              <div style="width: 26px; height: 26px; border-radius: 4px; background: var(--bg-card-subtle); border: 1px solid var(--border-subtle); color: var(--brand-primary); font-family: var(--font-display); font-size: 10px; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">${row.team.slice(0, 2).toUpperCase()}</div>
            `}
            <div>
              <strong style="color: var(--text-title); display: block; line-height: 1.2;">${row.team}</strong>
              <span style="font-size: 11px; color: var(--text-muted);">(${row.city})</span>
            </div>
          </div>
        </td>
        <td>${row.games}</td>
        <td>${row.w}</td>
        <td>${row.d}</td>
        <td>${row.l}</td>
        <td>${row.goals}</td>
        <td style="color: ${row.diff.startsWith('+') ? 'var(--accent-green)' : (row.diff.startsWith('-') ? 'var(--accent-red)' : 'inherit')};">${row.diff}</td>
        <td class="standings-pts-bold">${row.points}</td>
        <td>
          <div style="display: flex; gap: 3px; justify-content: center;">${formHtml}</div>
        </td>
      `;

      leagueStandingsBody.appendChild(tr);
    });
  }

  // =========================================================================
  // 5. TABS INTERACTION
  // =========================================================================
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');

      tabButtons.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add('active');
    });
  });

  // Tactical Board Click Connect
  document.querySelectorAll('.court-player-pin').forEach(pin => {
    pin.addEventListener('click', () => {
      const pName = pin.getAttribute('data-player-name');
      const found = data.players.find(p => p.name.includes(pName));
      if (found) {
        openModal(found);
      }
    });
  });

  // =========================================================================
  // 6. PLAYER DOSSIER MODAL (T-Bank Style Clean Sheet)
  // =========================================================================
  function openModal(p) {
    const hasPhoto = p.photo && p.photo.trim().length > 0;
    const initials = getInitials(p.name);
    const numDisplay = p.number && p.number !== '—' ? `№ ${p.number}` : 'Без номера';
    const ageDisplay = p.age ? `${p.age} лет` : '—';

    const isGk = p.position === 'Вратарь';

    let statsMatrixHtml = '';
    let extraStatsRows = '';

    if (isGk) {
      statsMatrixHtml = `
        <div class="modal-stats-matrix gk-matrix">
          <div>
            <div class="modal-stat-value">${p.matches_played ?? 1}</div>
            <div class="modal-stat-label">Матчи</div>
          </div>
          <div>
            <div class="modal-stat-value" style="color: var(--accent-red);">${p.goals_conceded ?? 0}</div>
            <div class="modal-stat-label">Пропущено</div>
          </div>
          <div>
            <div class="modal-stat-value" style="color: var(--accent-green);">${p.clean_sheets ?? 0}</div>
            <div class="modal-stat-label">На ноль</div>
          </div>
          <div>
            <div class="modal-stat-value" style="color: var(--text-title);">${p.penalty_6m_conceded ?? 0}</div>
            <div class="modal-stat-label">С 6м (пен)</div>
          </div>
          <div>
            <div class="modal-stat-value" style="color: var(--text-title);">${p.penalty_10m_conceded ?? 0}</div>
            <div class="modal-stat-label">С 10м (дабл)</div>
          </div>
        </div>
      `;

      extraStatsRows = `
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Пропущено голов:</span>
          <strong style="color: var(--accent-red); font-family: var(--font-display); font-size: 14px;">${p.goals_conceded ?? 0}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Матчей на ноль («сухие»):</span>
          <strong style="color: var(--accent-green); font-family: var(--font-display); font-size: 14px;">${p.clean_sheets ?? 0}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Пропущено с 6 метров (пенальти):</span>
          <strong style="color: var(--text-title); font-family: var(--font-display); font-size: 14px;">${p.penalty_6m_conceded ?? 0}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Пропущено с 10 метров (дабл-пенальти):</span>
          <strong style="color: var(--text-title); font-family: var(--font-display); font-size: 14px;">${p.penalty_10m_conceded ?? 0}</strong>
        </div>
      `;
    } else {
      statsMatrixHtml = `
        <div class="modal-stats-matrix">
          <div>
            <div class="modal-stat-value">${p.matches_played ?? 1}</div>
            <div class="modal-stat-label">Матчи</div>
          </div>
          <div>
            <div class="modal-stat-value" style="color: var(--accent-green);">${p.goals ?? 0}</div>
            <div class="modal-stat-label">Голы</div>
          </div>
          <div>
            <div class="modal-stat-value" style="color: var(--brand-primary);">${p.assists ?? 0}</div>
            <div class="modal-stat-label">Пасы</div>
          </div>
          <div>
            <div class="modal-stat-value" style="color: var(--accent-amber);">${p.yellow_cards ?? 0} / ${p.red_cards ?? 0}</div>
            <div class="modal-stat-label">ЖК / КК</div>
          </div>
        </div>
      `;

      extraStatsRows = `
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Забитые голы:</span>
          <strong style="color: var(--accent-green); font-family: var(--font-display); font-size: 14px;">${p.goals ?? 0}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Голевые передачи:</span>
          <strong style="color: var(--brand-primary); font-family: var(--font-display); font-size: 14px;">${p.assists ?? 0}</strong>
        </div>
      `;
    }

    playerModalBody.innerHTML = `
      <div class="modal-player-overview">
        <div class="modal-player-pic">
          ${hasPhoto
        ? `<img src="${p.photo}" alt="${p.name}" onerror="this.outerHTML='<div style=\\'display:flex;align-items:center;justify-content:center;height:100%;font-size:22px;font-weight:800;color:var(--brand-primary);\\'>${initials}</div>'">`
        : `<div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:22px;font-weight:800;color:var(--brand-primary);">${initials}</div>`
      }
        </div>
        <div>
          <h2 style="font-size: 18px; font-weight: 800; color: var(--text-title); margin-bottom: 4px;">${p.name}</h2>
          <div style="font-family: var(--font-display); font-size: 13px; font-weight: 800; color: var(--brand-primary); margin-bottom: 6px;">${numDisplay}</div>
          <span class="position-badge ${getPositionBadgeClass(p.position)}">${p.position}</span>
        </div>
      </div>

      ${statsMatrixHtml}

      <div style="margin-top: 18px; font-size: 13px; line-height: 1.6; color: var(--text-body);">
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Команда:</span>
          <strong style="color: var(--text-title);">${data.team_name} (Нижний Новгород)</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Турнир:</span>
          <strong style="color: var(--text-title);">${data.tournament}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Возраст:</span>
          <strong style="color: var(--text-title);">${ageDisplay}</strong>
        </div>
        ${extraStatsRows}
        <div style="display: flex; justify-content: space-between; padding: 8px 0;">
          <span style="color: var(--text-muted);">В базе Наградион:</span>
          <a href="${data.tournament_url}/player/${p.id}" target="_blank" rel="noopener" style="color: var(--brand-primary); font-weight: 700; text-decoration: underline;">
            ID ${p.id}
          </a>
        </div>
      </div>
    `;

    playerModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Click photo in modal to open full-res lightbox
    const modalPic = playerModalBody.querySelector('.modal-player-pic');
    if (modalPic && hasPhoto) {
      modalPic.setAttribute('title', 'Нажмите, чтобы открыть фотографию в полном размере');
      modalPic.addEventListener('click', () => {
        openPhotoLightbox(
          getHighResPhoto(p.photo),
          `${p.name} • ${p.position} ${numDisplay}`,
          `${data.team_name} (Нижний Новгород) • Наградион ID ${p.id}`
        );
      });
    }
  }

  function closePlayerModal() {
    playerModal.classList.remove('active');
    if (!photoLightbox || !photoLightbox.classList.contains('active')) {
      document.body.style.overflow = '';
    }
  }

  btnClosePlayerModal.addEventListener('click', closePlayerModal);

  playerModal.addEventListener('click', (e) => {
    if (e.target === playerModal) {
      closePlayerModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (photoLightbox && photoLightbox.classList.contains('active')) {
        closePhotoLightbox();
      } else if (playerModal && playerModal.classList.contains('active')) {
        closePlayerModal();
      }
    }
  });

  // =========================================================================
  // 7. CALENDAR EXPORT (.ICS)
  // =========================================================================
  window.downloadICS = function (team1, team2, venue) {
    const icsContent = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//NNDEPSPORT//RU',
      'CALSCALE:GREGORIAN',
      'METHOD:PUBLISH',
      'BEGIN:VEVENT',
      'SUMMARY:Матч: ' + team1 + ' vs ' + team2,
      'DESCRIPTION:Матч Первой лиги по мини-футболу. Подробнее: ' + data.tournament_url,
      'LOCATION:' + venue + ', Нижний Новгород',
      'DTSTART:20261019T181000Z', // 21:10 MSK is 18:10 UTC
      'DTEND:20261019T192000Z',
      'STATUS:CONFIRMED',
      'END:VEVENT',
      'END:VCALENDAR'
    ].join('\r\n');

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.setAttribute('download', 'match_doza_agro.ics');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (btnDownloadIcs) {
    btnDownloadIcs.addEventListener('click', () => {
      window.downloadICS('Продтерминал', 'Доза Агро', 'ФОК «Приокский»');
    });
  }

  // Background Theme Switcher
  const bgThemeSelect = document.getElementById('bgThemeSelect');
  function applyBgTheme(theme) {
    document.body.classList.remove('bg-modern-cyan', 'bg-modern-azure', 'bg-classic', 'bg-none');
    document.body.classList.add(`bg-${theme}`);
  }

  if (bgThemeSelect) {
    const savedBg = localStorage.getItem('site_bg_mode') || 'classic';
    bgThemeSelect.value = savedBg;
    applyBgTheme(savedBg);

    bgThemeSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      localStorage.setItem('site_bg_mode', val);
      applyBgTheme(val);
    });
  }

  // Initial render
  renderSquad();
  renderCalendar();
  renderStandings();
});
