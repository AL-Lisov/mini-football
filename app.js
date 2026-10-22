/**
 * МФК «ДОЗА АГРО» - APPLICATION CONTROLLER
 * Juventus Brutalism + EA FC 24 FUT Ultimate Team Gamification
 * Dynamic 3D Tilt • Live Countdown • Interactive Tactics 5x5
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
  const tabButtons = document.querySelectorAll('.pro-tab-item, .t-tab-item');
  const tabPanels = document.querySelectorAll('.tab-view-panel');

  const playerModal = document.getElementById('playerModal');
  const playerModalBody = document.getElementById('playerModalBody');
  const btnClosePlayerModal = document.getElementById('btnClosePlayerModal');

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

  // =========================================================================
  // 1. FUT RATINGS & STATS ENGINE
  // =========================================================================
  const playerCustomStats = {
    // Lisov Alexander (Goalkeeper, 31 yo)
    '1333860': {
      ovr: 89,
      roleName: 'THE WALL',
      cardTier: 'gold-special',
      isGk: true,
      stats: { REF: 92, SAV: 90, HAN: 88, POS: 90, KIC: 86, PHY: 87 }
    },
    // Orekhov Alexander (Goalkeeper, 23 yo)
    '1333863': {
      ovr: 88,
      roleName: 'SAFE HANDS',
      cardTier: 'gold-special',
      isGk: true,
      stats: { REF: 90, SAV: 88, HAN: 87, POS: 88, KIC: 85, PHY: 86 }
    },
    // Balashov Maxim (Universal / Captain, 25 yo)
    '1190379': {
      ovr: 87,
      roleName: 'CAPITANO',
      cardTier: 'gold-special',
      isGk: false,
      stats: { PAC: 88, SHO: 85, PAS: 87, DRI: 88, DEF: 82, PHY: 85 }
    },
    // Dragov Anton (Forward, 30 yo)
    '1333855': {
      ovr: 86,
      roleName: 'STRIKER',
      cardTier: 'gold',
      isGk: false,
      stats: { PAC: 87, SHO: 88, PAS: 82, DRI: 85, DEF: 65, PHY: 84 }
    },
    // Barinov Alexander (Defender, 29 yo)
    '1333853': {
      ovr: 85,
      roleName: 'COMMANDER',
      cardTier: 'gold',
      isGk: false,
      stats: { PAC: 82, SHO: 74, PAS: 84, DRI: 80, DEF: 88, PHY: 86 }
    }
  };

  function getPlayerFUTStats(player) {
    if (playerCustomStats[player.id]) {
      return playerCustomStats[player.id];
    }
    const isGk = player.position === 'Вратарь';
    const baseOvr = 82 + ((parseInt(player.id, 10) % 4));
    if (isGk) {
      return {
        ovr: baseOvr,
        roleName: 'GOALKEEPER',
        cardTier: 'gold',
        isGk: true,
        stats: { REF: baseOvr + 2, SAV: baseOvr + 1, HAN: baseOvr, POS: baseOvr, KIC: baseOvr - 2, PHY: baseOvr }
      };
    }
    return {
      ovr: baseOvr,
      roleName: player.position.toUpperCase(),
      cardTier: 'gold',
      isGk: false,
      stats: {
        PAC: 83 + (parseInt(player.id) % 6),
        SHO: 80 + (parseInt(player.id) % 5),
        PAS: 81 + (parseInt(player.id) % 6),
        DRI: 82 + (parseInt(player.id) % 5),
        DEF: player.position === 'Защитник' ? 84 : 76,
        PHY: 81 + (parseInt(player.id) % 4)
      }
    };
  }

  function getPosShortCode(pos) {
    switch (pos) {
      case 'Вратарь': return 'ВРТ';
      case 'Защитник': return 'ЗАЩ';
      case 'Универсал': return 'УНВ';
      case 'Нападающий': return 'НАП';
      case 'Полевой': return 'ПОЛ';
      default: return 'ИГР';
    }
  }

  function getPosClass(pos) {
    switch (pos) {
      case 'Вратарь': return 'pos-gk';
      case 'Защитник': return 'pos-def';
      case 'Универсал': return 'pos-uni';
      case 'Нападающий': return 'pos-fwd';
      case 'Полевой': return 'pos-pol';
      default: return '';
    }
  }

  function getInitials(fullName) {
    if (!fullName) return 'ДА';
    const parts = fullName.trim().split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return parts[0].slice(0, 2).toUpperCase();
  }

  function getHighResPhoto(url) {
    if (!url) return '';
    return url.replace('/small/', '/normal/');
  }

  // =========================================================================
  // 2. PHOTO LIGHTBOX CONTROLLER
  // =========================================================================
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
        'Нижний Новгород • Чемпионат по мини-футболу'
      );
    });
  }

  if (leaderItemPavlyuk) {
    leaderItemPavlyuk.addEventListener('click', () => {
      openPhotoLightbox(
        'https://img.nagradion.ru/images/normal/m/playerac2d91dcabaf0009494f10c994c5ffff.jpg',
        'Павлюк Александр • Руководитель МФК «Доза Агро»',
        'Первая лига Нижнего Новгорода'
      );
    });
  }

  if (leaderItemBalashov) {
    leaderItemBalashov.addEventListener('click', () => {
      openPhotoLightbox(
        'https://img.nagradion.ru/images/normal/m/player0ed34af96bbb2dcc08bc7340b192dc53.jpg',
        'Балашов Максим • Тренер и капитан команды',
        'МФК «Доза Агро» • Игровой номер 17'
      );
    });
  }

  // =========================================================================
  // 3. SQUAD RENDERING (FUT CARDS + 3D TILT EFFECT)
  // =========================================================================
  function renderSquad() {
    if (!squadGroupedOutput) return;
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
          <div style="font-size: 16px; font-weight: 800; color: #FFFFFF; text-transform: uppercase; margin-bottom: 6px;">Игроков не найдено</div>
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

      // Group Header
      const headerDiv = document.createElement('div');
      headerDiv.className = 'squad-group-header';
      headerDiv.innerHTML = `
        <h2 class="squad-group-title">
          <span>${grp.title}</span>
          <span class="squad-group-count">${grpPlayers.length}</span>
        </h2>
      `;
      groupWrapper.appendChild(headerDiv);

      if (currentViewMode === 'table') {
        // Table Mode
        const tableWrap = document.createElement('div');
        tableWrap.className = 'pro-squad-table-wrap';
        let tHtml = `
          <table class="pro-squad-table">
            <thead>
              <tr>
                <th class="col-sq-num">№</th>
                <th class="col-sq-player" style="text-align: left;">Игрок</th>
                <th class="col-sq-pos">Позиция</th>
                <th class="col-sq-age">Возраст</th>
                <th class="col-sq-ovr">OVR</th>
                <th class="col-sq-matches">Матчи</th>
                <th class="col-sq-stat">${grp.key === 'Вратарь' ? 'На ноль / Проп' : 'Голы / Пасы'}</th>
              </tr>
            </thead>
            <tbody>
        `;

        grpPlayers.forEach(p => {
          const fut = getPlayerFUTStats(p);
          const initials = getInitials(p.name);
          const hasPhoto = p.photo && p.photo.trim().length > 0;
          const numStr = p.number && p.number !== '—' ? p.number : '—';
          const statCol = fut.isGk
            ? `<strong class="sq-stat-bold">${p.clean_sheets ?? 1}</strong> / <span class="sq-stat-dim">${p.goals_conceded ?? 0}</span>`
            : `<strong class="sq-stat-bold">${p.goals ?? 0}</strong> / <span class="sq-stat-dim">${p.assists ?? 0}</span>`;

          tHtml += `
            <tr data-id="${p.id}">
              <td class="col-sq-num"><span class="sq-table-num">${numStr}</span></td>
              <td class="col-sq-player">
                <div class="pro-table-person">
                  ${hasPhoto
                    ? `<img src="${p.photo}" class="pro-table-thumb" alt="${p.name}">`
                    : `<div class="pro-table-initials">${initials}</div>`
                  }
                  <strong class="pro-table-name">${p.name}</strong>
                </div>
              </td>
              <td class="col-sq-pos"><span class="pro-table-pos-pill">${p.position}</span></td>
              <td class="col-sq-age">${p.age ? p.age + ' лет' : '—'}</td>
              <td class="col-sq-ovr"><span class="pro-table-ovr">${fut.ovr}</span></td>
              <td class="col-sq-matches">${p.matches_played ?? 1}</td>
              <td class="col-sq-stat">${statCol}</td>
            </tr>
          `;
        });

        tHtml += `</tbody></table>`;
        tableWrap.innerHTML = tHtml;

        tableWrap.querySelectorAll('tbody tr').forEach(tr => {
          const pid = tr.getAttribute('data-id');
          const pObj = data.players.find(x => x.id === pid);
          if (pObj) tr.addEventListener('click', () => openModal(pObj));
        });

        groupWrapper.appendChild(tableWrap);
      } else {
        // FUT Cards Grid
        const cardsGrid = document.createElement('div');
        cardsGrid.className = 'fut-cards-grid';

        grpPlayers.forEach(p => {
          const fut = getPlayerFUTStats(p);
          const initials = getInitials(p.name);
          const hasPhoto = p.photo && p.photo.trim().length > 0;
          const numStr = p.number && p.number !== '—' ? p.number : '—';
          const posCode = getPosShortCode(p.position);
          const posCls = getPosClass(p.position);

          // Split surname and first name
          const nameParts = p.name.trim().split(/\s+/);
          const surname = nameParts[0] || p.name;
          const firstName = nameParts.slice(1).join(' ');

          // Stats grid (Hex bars)
          let statsGridHtml = '';
          for (const [key, val] of Object.entries(fut.stats)) {
            statsGridHtml += `
              <div class="fut-stat-cell">
                <span class="fut-stat-val">${val}</span>
                <span class="fut-stat-lbl">${key}</span>
              </div>
            `;
          }

          // Amateur stats ribbon
          const amateurHtml = fut.isGk ? `
            <div class="fut-amateur-row">
              <span class="fut-amateur-item clean-sheet" title="Матчи на ноль">НА НОЛЬ: <strong>${p.clean_sheets ?? 1}</strong></span>
              <span>•</span>
              <span class="fut-amateur-item" title="Пропущено голов">ПРОП: <strong>${p.goals_conceded ?? 0}</strong></span>
              <span>•</span>
              <span class="fut-amateur-item" title="Пенальти 6м / 10м">ПЕН: <strong>${p.penalty_6m_conceded ?? 0}/${p.penalty_10m_conceded ?? 0}</strong></span>
            </div>
          ` : `
            <div class="fut-amateur-row">
              <span class="fut-amateur-item" title="Сыграно матчей">ИГРЫ: <strong>${p.matches_played ?? 1}</strong></span>
              <span>•</span>
              <span class="fut-amateur-item" title="Забито голов">ГОЛЫ: <strong>${p.goals ?? 0}</strong></span>
              <span>•</span>
              <span class="fut-amateur-item" title="Голевые передачи">ПАСЫ: <strong>${p.assists ?? 0}</strong></span>
            </div>
          `;

          const card = document.createElement('div');
          card.className = 'fut-card';
          card.setAttribute('data-id', p.id);

          card.innerHTML = `
            <div class="fut-card-inner">
              <div class="fut-hologram"></div>
              <div class="fut-jersey-watermark">${numStr !== '—' ? numStr : ''}</div>

              <!-- Topbar: OVR + Position + Club -->
              <div class="fut-card-topbar">
                <div class="fut-rating-block">
                  <span class="fut-ovr-number">${fut.ovr}</span>
                  <span class="fut-pos-badge ${posCls}">${posCode}</span>
                </div>
                <img src="${data.team_logo}" alt="Доза Агро" class="fut-club-shield" onerror="this.style.display='none'">
              </div>

              <!-- Portrait Area -->
              <div class="fut-portrait-wrap">
                ${hasPhoto
                  ? `<img src="${p.photo}" class="fut-player-img" alt="${p.name}" loading="lazy" onerror="this.outerHTML='<div class=\\'fut-initials-fallback\\'>${initials}</div>'">`
                  : `<div class="fut-initials-fallback">${initials}</div>`
                }
              </div>

              <!-- Nameplate -->
              <div class="fut-nameplate">
                <div class="fut-surname" title="${p.name}">${surname}</div>
                <div class="fut-firstname">${firstName} • ${p.age ? p.age + ' лет' : '№' + numStr}</div>
              </div>

              <!-- Attribute Hex Grid -->
              <div class="fut-stats-grid">
                ${statsGridHtml}
              </div>

              <!-- Amateur Stats -->
              ${amateurHtml}
            </div>
          `;

          // 3D Tilt & Holographic tracking on mousemove
          card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.03, 1.03, 1.03)`;
            card.style.setProperty('--mouse-x', `${(x / rect.width) * 100}%`);
            card.style.setProperty('--mouse-y', `${(y / rect.height) * 100}%`);
          });

          card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
          });

          // Open Modal on click
          card.addEventListener('click', () => openModal(p));

          cardsGrid.appendChild(card);
        });

        groupWrapper.appendChild(cardsGrid);
      }

      squadGroupedOutput.appendChild(groupWrapper);
    });
  }

  // Position filter button listeners
  if (positionFilters) {
    positionFilters.querySelectorAll('.t-filter-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        positionFilters.querySelectorAll('.t-filter-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentPosition = btn.getAttribute('data-pos');
        renderSquad();
      });
    });
  }

  // Search field listener
  if (squadSearchField) {
    squadSearchField.addEventListener('input', (e) => {
      searchVal = e.target.value;
      renderSquad();
    });
  }

  // View mode switcher
  if (btnModeCards && btnModeTable) {
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
  }

  // =========================================================================
  // 4. CALENDAR & MATCHES (Broadcast Cards)
  // =========================================================================
  function renderCalendar() {
    if (!calendarMatchList) return;
    calendarMatchList.innerHTML = '';

    data.matches.forEach(m => {
      const card = document.createElement('div');
      const isCompleted = m.status === 'completed';
      const isNext = m.status === 'next';
      card.className = `rfs-match-card ${isNext ? 'is-spotlight' : ''}`;

      const isDozAHome = m.team1.includes('Доза Агро');
      const isDozAAway = m.team2.includes('Доза Агро');

      let statusBadgeText = '1-й круг';
      let statusBadgeColor = 'var(--text-muted)';
      if (isCompleted) {
        statusBadgeText = 'Завершен';
        statusBadgeColor = 'var(--neon-volt)';
      } else if (isNext) {
        statusBadgeText = 'Ближайший матч';
        statusBadgeColor = 'var(--neon-cyan)';
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
            <div class="score-value-bold" style="${isCompleted ? 'border-color: var(--neon-volt); color: var(--neon-volt);' : ''}">${m.score}</div>
            <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: ${statusBadgeColor}; margin-top: 4px;">
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
          <div style="margin: 8px 0 14px; padding: 10px 14px; background: rgba(212, 255, 0, 0.05); border: 1px solid var(--border-neon); border-radius: var(--radius-xs); font-size: 12px; color: #FFFFFF; display: flex; align-items: center; gap: 8px;">
            <strong style="color: var(--neon-volt);">Стена команды:</strong> <span>${m.note}</span>
          </div>
        ` : ''}

        <div class="match-footer-row">
          <div class="match-location-link">
            <strong>${m.venue}</strong>
            <a href="https://yandex.ru/maps/?text=${encodeURIComponent(m.venue + ' Нижний Новгород')}" target="_blank" rel="noopener">На карте</a>
          </div>

          <div style="display: flex; gap: 8px;">
            <a href="${data.tournament_url}/match/${m.match_id}" target="_blank" rel="noopener" class="pro-btn" style="background: rgba(255,255,255,0.06); color: #fff; border: 1px solid var(--border-card); font-size: 11px; padding: 6px 12px;">
              ${isCompleted ? 'Протокол матча' : 'Превью матча'}
            </a>
            ${isNext ? `
              <button class="pro-btn btn-neon" style="font-size: 11px; padding: 6px 12px;" onclick="window.downloadICS('${m.team1}', '${m.team2}', '${m.venue}')">
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
  // 5. STANDINGS TABLE (Serie A / Champions League Pro Responsive Table)
  // =========================================================================
  function renderStandings() {
    if (!leagueStandingsBody) return;
    leagueStandingsBody.innerHTML = '';

    data.standings.forEach(row => {
      const isMyTeam = row.team === 'Доза Агро';

      const formHtml = row.form.map(f => {
        const cls = f === 'W' ? 'win' : (f === 'D' ? 'draw' : 'loss');
        const letter = f === 'W' ? 'В' : (f === 'D' ? 'Н' : 'П');
        return `<span class="form-pill-tag ${cls}">${letter}</span>`;
      }).join('');

      // Main Row
      const tr = document.createElement('tr');
      tr.className = `standings-team-row ${isMyTeam ? 'highlight-row' : ''}`;
      tr.setAttribute('data-pos', row.pos);

      tr.innerHTML = `
        <td class="col-pos"><span class="pos-badge ${row.pos <= 3 ? 'medal-zone' : ''}">${row.pos}</span></td>
        <td class="col-team col-club-left">
          <div class="team-cell-wrap">
            ${row.shield ? `
              <img src="${row.shield}" alt="${row.team}" class="standings-shield" onerror="this.style.display='none'">
            ` : `
              <div class="standings-shield-initials">${row.team.slice(0, 2).toUpperCase()}</div>
            `}
            <div class="team-info-box">
              <strong class="team-title-text ${isMyTeam ? 'my-club-name' : ''}">${row.team}</strong>
              <span class="team-meta-sub">${row.city}</span>
              <!-- Mobile inline compact record: 1В 0Н 0П • Мячи: 3-1 -->
              <div class="team-mobile-substat">
                <span>${row.w}В ${row.d}Н ${row.l}П</span>
                <span class="dot-sep">•</span>
                <span>Мячи: ${row.goals}</span>
              </div>
            </div>
          </div>
        </td>
        <td class="col-games">${row.games}</td>
        <td class="col-wins col-optional">${row.w}</td>
        <td class="col-draws col-optional">${row.d}</td>
        <td class="col-losses col-optional">${row.l}</td>
        <td class="col-goals col-optional">${row.goals}</td>
        <td class="col-diff ${row.diff.startsWith('+') ? 'pos-diff' : (row.diff.startsWith('-') ? 'neg-diff' : '')}">${row.diff}</td>
        <td class="col-pts"><span class="standings-pts-badge">${row.points}</span></td>
        <td class="col-form col-optional">
          <div class="form-pills-row">${formHtml}</div>
        </td>
      `;

      // Expandable Drawer Row for Mobile
      const drawerTr = document.createElement('tr');
      drawerTr.className = 'standings-drawer-row';
      drawerTr.id = `drawer-pos-${row.pos}`;
      drawerTr.style.display = 'none';

      drawerTr.innerHTML = `
        <td colspan="10" class="standings-drawer-cell">
          <div class="standings-drawer-content">
            <div class="drawer-stat-grid">
              <div class="drawer-stat-item"><span class="drawer-lbl">Игры</span><strong>${row.games}</strong></div>
              <div class="drawer-stat-item"><span class="drawer-lbl">Победы</span><strong style="color: var(--accent-green);">${row.w}</strong></div>
              <div class="drawer-stat-item"><span class="drawer-lbl">Ничьи</span><strong style="color: var(--neon-amber);">${row.d}</strong></div>
              <div class="drawer-stat-item"><span class="drawer-lbl">Поражения</span><strong style="color: var(--accent-red);">${row.l}</strong></div>
              <div class="drawer-stat-item"><span class="drawer-lbl">Забито/Проп</span><strong>${row.goals}</strong></div>
              <div class="drawer-stat-item"><span class="drawer-lbl">Разница</span><strong>${row.diff}</strong></div>
              <div class="drawer-stat-item"><span class="drawer-lbl">Очки</span><strong style="color: var(--neon-volt); font-size: 16px;">${row.points}</strong></div>
            </div>
            <div class="drawer-footer-line">
              <span class="drawer-lbl">Город: ${row.city}</span>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span class="drawer-lbl">Форма:</span>
                <div style="display: flex; gap: 4px;">${formHtml}</div>
              </div>
            </div>
          </div>
        </td>
      `;

      // Toggle drawer on click
      tr.addEventListener('click', () => {
        const isOpen = drawerTr.classList.contains('is-open');

        // Close all drawers and un-highlight rows
        document.querySelectorAll('.standings-drawer-row').forEach(d => {
          d.classList.remove('is-open');
          d.style.display = 'none';
        });
        document.querySelectorAll('.standings-team-row').forEach(r => {
          r.classList.remove('is-expanded');
        });

        // Open clicked team drawer if it was not already open
        if (!isOpen) {
          drawerTr.classList.add('is-open');
          drawerTr.style.display = window.innerWidth <= 640 ? 'block' : 'table-row';
          tr.classList.add('is-expanded');
        }
      });

      leagueStandingsBody.appendChild(tr);
      leagueStandingsBody.appendChild(drawerTr);
    });
  }

  // =========================================================================
  // 6. STICKY SUBNAV & SMOOTH SCROLL SPY
  // =========================================================================
  const navPills = document.querySelectorAll('.juve-nav-pill');
  const anchorLinks = document.querySelectorAll('a[href^="#section-"]');

  anchorLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      const targetSec = document.querySelector(href);
      if (targetSec) {
        e.preventDefault();
        const headerOffset = 110;
        const elementPosition = targetSec.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // Scroll spy to highlight active pill in sticky subnav
  const observedSections = document.querySelectorAll('section[id^="section-"]');
  window.addEventListener('scroll', () => {
    let currentId = '';
    const scrollPos = window.scrollY + 140;

    observedSections.forEach(sec => {
      if (scrollPos >= sec.offsetTop) {
        currentId = sec.getAttribute('id');
      }
    });

    if (currentId) {
      navPills.forEach(pill => {
        pill.classList.toggle('active', pill.getAttribute('href') === `#${currentId}`);
      });
    }
  }, { passive: true });

  // =========================================================================
  // 7. TACTICAL PITCH 5x5 (Cyber Formations)
  // =========================================================================
  const formations = {
    diamond: {
      pinGk: { top: '86%', left: '50%' },
      pinDef: { top: '65%', left: '50%' },
      pinLw: { top: '42%', left: '22%' },
      pinRw: { top: '42%', left: '78%' },
      pinFwd: { top: '18%', left: '50%' }
    },
    box: {
      pinGk: { top: '86%', left: '50%' },
      pinDef: { top: '62%', left: '30%' },
      pinLw: { top: '62%', left: '70%' },
      pinRw: { top: '25%', left: '30%' },
      pinFwd: { top: '25%', left: '70%' }
    },
    pyramid: {
      pinGk: { top: '86%', left: '50%' },
      pinLw: { top: '62%', left: '20%' },
      pinDef: { top: '66%', left: '50%' },
      pinRw: { top: '62%', left: '80%' },
      pinFwd: { top: '20%', left: '50%' }
    }
  };

  const formationBtns = document.querySelectorAll('.formation-btn');
  formationBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      formationBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const formKey = btn.getAttribute('data-formation');
      const cfg = formations[formKey];
      if (!cfg) return;

      for (const [pinId, coords] of Object.entries(cfg)) {
        const pinEl = document.getElementById(pinId);
        if (pinEl) {
          pinEl.style.top = coords.top;
          pinEl.style.left = coords.left;
        }
      }
    });
  });

  // Click player pin on tactical court opens player modal
  document.querySelectorAll('.court-player-pin').forEach(pin => {
    pin.addEventListener('click', () => {
      const pName = pin.getAttribute('data-player-name');
      const found = data.players.find(p => p.name.includes(pName));
      if (found) openModal(found);
    });
  });

  // =========================================================================
  // 8. LIVE COUNTDOWN TIMER (Next Match)
  // =========================================================================
  function startCountdown() {
    // Next match: 26 October 2026, 19:30 MSK
    const targetDate = new Date('2026-10-26T19:30:00+03:00').getTime();

    const cdDays = document.getElementById('cdDays');
    const cdHours = document.getElementById('cdHours');
    const cdMins = document.getElementById('cdMins');
    const cdSecs = document.getElementById('cdSecs');

    if (!cdDays || !cdHours || !cdMins || !cdSecs) return;

    function update() {
      const now = new Date().getTime();
      let diff = targetDate - now;

      if (diff <= 0) {
        cdDays.textContent = '00';
        cdHours.textContent = '00';
        cdMins.textContent = '00';
        cdSecs.textContent = '00';
        return;
      }

      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const secs = Math.floor((diff % (1000 * 60)) / 1000);

      cdDays.textContent = String(days).padStart(2, '0');
      cdHours.textContent = String(hours).padStart(2, '0');
      cdMins.textContent = String(mins).padStart(2, '0');
      cdSecs.textContent = String(secs).padStart(2, '0');
    }

    update();
    setInterval(update, 1000);
  }

  // =========================================================================
  // 8.1 LIVE DIGITAL SPORTS CLOCK (Juventus Match Ribbon - Moscow UTC+3)
  // =========================================================================
  function startLiveClock() {
    const clockEl = document.getElementById('liveDigitalClock');
    const dateEl = document.getElementById('liveDigitalDate');
    if (!clockEl && !dateEl) return;

    function tick() {
      const now = new Date();
      // Formatted Moscow time
      const timeStr = now.toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'Europe/Moscow'
      });

      const daysRu = ['ВОСКРЕСЕНЬЕ', 'ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА'];
      const monthsRu = ['ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ', 'МАЯ', 'ИЮНЯ', 'ИЮЛЯ', 'АВГУСТА', 'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ', 'ДЕКАБРЯ'];

      const dayOfWeek = daysRu[now.getDay()];
      const dayNum = now.getDate();
      const monthName = monthsRu[now.getMonth()];
      const dateStr = `${dayOfWeek}, ${dayNum} ${monthName}`;

      if (clockEl) clockEl.textContent = timeStr;
      if (dateEl) dateEl.textContent = dateStr;
    }

    tick();
    setInterval(tick, 1000);
  }

  // =========================================================================
  // 9. PLAYER DOSSIER MODAL
  // =========================================================================
  function openModal(p) {
    if (!playerModal || !playerModalBody) return;

    const fut = getPlayerFUTStats(p);
    const initials = getInitials(p.name);
    const hasPhoto = p.photo && p.photo.trim().length > 0;
    const numStr = p.number && p.number !== '—' ? '№' + p.number : '—';
    const isGk = p.position === 'Вратарь';

    const ageDisplay = p.age ? `${p.age} лет` : 'Не указан';

    const extraStatsRows = isGk ? `
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Матчи «на ноль»:</span>
        <strong style="color: var(--neon-volt);">${p.clean_sheets ?? 1} (100% сухая серия)</strong>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Пропущено голов:</span>
        <strong style="color: var(--neon-volt);">${p.goals_conceded ?? 0}</strong>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Пропущено с 6 метров (пенальти):</span>
        <strong style="color: #FFFFFF;">${p.penalty_6m_conceded ?? 0}</strong>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Пропущено с 10 метров (дабл-пен):</span>
        <strong style="color: #FFFFFF;">${p.penalty_10m_conceded ?? 0}</strong>
      </div>
    ` : `
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Сыграно матчей:</span>
        <strong style="color: #FFFFFF;">${p.matches_played ?? 1}</strong>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Забито голов:</span>
        <strong style="color: var(--neon-volt);">${p.goals ?? 0}</strong>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Голевые передачи:</span>
        <strong style="color: #FFFFFF;">${p.assists ?? 0}</strong>
      </div>
    `;

    playerModalBody.innerHTML = `
      <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 24px; padding-bottom: 18px; border-bottom: 1px solid var(--border-card);">
        <div style="width: 80px; height: 80px; border-radius: var(--radius-md); background: #1B2135; border: 2px solid var(--neon-volt); overflow: hidden; flex-shrink: 0; display: flex; align-items: center; justify-content: center; cursor: pointer;" title="Нажмите для увеличения фото">
          ${hasPhoto
            ? `<img src="${p.photo}" alt="${p.name}" style="width:100%;height:100%;object-fit:cover;">`
            : `<span style="font-family: var(--font-display); font-size: 24px; font-weight: 900; color: var(--neon-volt);">${initials}</span>`
          }
        </div>
        <div>
          <h2 style="font-family: var(--font-display); font-size: 22px; font-weight: 900; color: #FFFFFF; text-transform: uppercase; line-height: 1.1; margin-bottom: 6px;">${p.name}</h2>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="pro-pill pill-neon">${p.position}</span>
            <span style="font-family: var(--font-display); font-size: 14px; font-weight: 800; color: var(--neon-cyan);">OVR ${fut.ovr}</span>
            <span style="font-size: 13px; color: var(--text-muted); font-weight: 700;">${numStr}</span>
          </div>
        </div>
      </div>

      <div style="font-size: 13px;">
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Команда:</span>
          <strong style="color: #FFFFFF;">МФК «Доза Агро»</strong>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
          <span style="color: var(--text-muted);">Возраст:</span>
          <strong style="color: #FFFFFF;">${ageDisplay}</strong>
        </div>
        ${extraStatsRows}
        <div style="display: flex; justify-content: space-between; padding: 10px 0;">
          <span style="color: var(--text-muted);">В базе Наградион:</span>
          <a href="${data.tournament_url}/player/${p.id}" target="_blank" rel="noopener" style="color: var(--neon-volt); font-weight: 700; text-decoration: underline;">
            ID ${p.id}
          </a>
        </div>
      </div>
    `;

    playerModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Click photo in modal to open lightbox
    const modalPic = playerModalBody.querySelector('img');
    if (modalPic && hasPhoto) {
      modalPic.addEventListener('click', () => {
        openPhotoLightbox(
          getHighResPhoto(p.photo),
          `${p.name} • ${p.position} ${numStr}`,
          `${data.team_name} • Наградион ID ${p.id}`
        );
      });
    }
  }

  function closeModal() {
    if (!playerModal) return;
    playerModal.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (btnClosePlayerModal) {
    btnClosePlayerModal.addEventListener('click', closeModal);
  }

  if (playerModal) {
    playerModal.addEventListener('click', (e) => {
      if (e.target === playerModal) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (photoLightbox && photoLightbox.classList.contains('active')) {
        closePhotoLightbox();
      } else {
        closeModal();
      }
    }
  });

  // =========================================================================
  // 10. BACKGROUND ATMOSPHERE SWITCHER & MOBILE BURGER MENU
  // =========================================================================
  const bgThemeSelect = document.getElementById('bgThemeSelect');
  const bgThemeSelectMobile = document.getElementById('bgThemeSelectMobile');
  const mobileBurgerBtn = document.getElementById('mobileBurgerBtn');
  const mobileMenu = document.getElementById('mobileMenu');

  // Background Theme Sync
  const savedBg = localStorage.getItem('doza_bg_theme') || 'stadium-dark';
  document.body.setAttribute('data-bg', savedBg);

  if (bgThemeSelect) {
    bgThemeSelect.value = savedBg;
    bgThemeSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      document.body.setAttribute('data-bg', val);
      if (bgThemeSelectMobile) bgThemeSelectMobile.value = val;
      localStorage.setItem('doza_bg_theme', val);
    });
  }

  if (bgThemeSelectMobile) {
    bgThemeSelectMobile.value = savedBg;
    bgThemeSelectMobile.addEventListener('change', (e) => {
      const val = e.target.value;
      document.body.setAttribute('data-bg', val);
      if (bgThemeSelect) bgThemeSelect.value = val;
      localStorage.setItem('doza_bg_theme', val);
    });
  }

  // Mobile Burger & Menu Controller
  if (mobileBurgerBtn && mobileMenu) {
    mobileBurgerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = mobileMenu.classList.toggle('is-open');
      mobileBurgerBtn.classList.toggle('is-active', isOpen);
      mobileBurgerBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close when clicking any link inside mobile menu
    mobileMenu.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('is-open');
        mobileBurgerBtn.classList.remove('is-active');
        mobileBurgerBtn.setAttribute('aria-expanded', 'false');
      });
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!mobileMenu.contains(e.target) && e.target !== mobileBurgerBtn && !mobileBurgerBtn.contains(e.target)) {
        mobileMenu.classList.remove('is-open');
        mobileBurgerBtn.classList.remove('is-active');
        mobileBurgerBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // =========================================================================
  // 11. CALENDAR EXPORT (.ICS)
  // =========================================================================
  window.downloadICS = function (team1, team2, venue) {
    const icsContent = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//NNDEPSPORT//Doza Agro Match//RU',
      'CALSCALE:GREGORIAN',
      'METHOD:PUBLISH',
      'BEGIN:VEVENT',
      'SUMMARY:' + team1 + ' - ' + team2 + ' (Первая лига)',
      'DESCRIPTION:Матч Чемпионата Нижнего Новгорода по мини-футболу (Футзал 5х5)',
      'LOCATION:' + venue + ' Нижний Новгород',
      'DTSTART:20261026T163000Z',
      'DTEND:20261026T174500Z',
      'STATUS:CONFIRMED',
      'END:VEVENT',
      'END:VCALENDAR'
    ].join('\r\n');

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'match_doza_agro.ics');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // =========================================================================
  // 12. INITIALIZATION
  // =========================================================================
  renderSquad();
  renderCalendar();
  renderStandings();
  startCountdown();
  startLiveClock();
});
