from pathlib import Path
import re

ROOT = Path('_posts')

# Chỉ thay các từ tiếng Anh không cần thiết trong phần người đọc nhìn thấy.
# Các thuật ngữ phổ biến trong công nghệ như gear, gaming, AI, RAM, SSD, CPU, GPU,
# benchmark, creator, hub, dock, Wi‑Fi, Bluetooth, USB, OLED... được giữ lại.
REPLACEMENTS = [
    (r'\bbottleneck\b', 'điểm nghẽn'),
    (r'\bworkload\b', 'khối lượng công việc'),
    (r'\bdowntime\b', 'thời gian gián đoạn'),
    (r'\bworkflow\b', 'quy trình làm việc'),
    (r'\bROI\b', 'mức độ đáng tiền'),
    (r'\btrade[- ]?off\b', 'sự đánh đổi'),
    (r'\bvendor claim\b', 'thông tin hãng công bố'),
    (r'\blab claim\b', 'con số hãng đo trong phòng thử nghiệm'),
    (r'\bclaim\b', 'thông tin hãng công bố'),
    (r'\bscaling\b', 'tỷ lệ hiển thị'),
    (r'\brefresh rate\b', 'tần số quét'),
    (r'\bcolor profile\b', 'hồ sơ màu'),
    (r'\bpolling rate\b', 'tần số phản hồi'),
    (r'\bform factor\b', 'kiểu dáng'),
    (r'\bthroughput\b', 'tốc độ truyền dữ liệu'),
    (r'\bspec sheet\b', 'bảng thông số'),
    (r'\bspecs\b', 'thông số'),
    (r'\bspec\b', 'thông số'),
    (r'\buse case\b', 'nhu cầu sử dụng'),
    (r'\bfuture[- ]?proofing\b', 'khả năng dùng lâu dài'),
    (r'\bfuture[- ]?proof\b', 'dùng lâu dài'),
    (r'\blocal AI\b', 'AI chạy trực tiếp trên máy'),
    (r'\bproductivity\b', 'hiệu quả làm việc'),
    (r'\bsustained performance\b', 'hiệu năng duy trì lâu'),
    (r'\bburst performance\b', 'hiệu năng trong tác vụ ngắn'),
    (r'\bpower user\b', 'người dùng nặng'),
    (r'\bdaily driver\b', 'thiết bị chính dùng hằng ngày'),
    (r'\breal[- ]?world\b', 'thực tế'),
    (r'\bhands[- ]?on\b', 'trải nghiệm trực tiếp'),
    (r'\bthermal budget\b', 'khả năng tản nhiệt'),
    (r'\bthermal throttling\b', 'giảm hiệu năng vì nhiệt'),
    (r'\bthrottling\b', 'giảm hiệu năng vì nhiệt'),
    (r'\blatency\b', 'độ trễ'),
    (r'\bheadroom\b', 'phần hiệu năng còn dư'),
    (r'\bbattery life\b', 'thời lượng pin'),
]

EXACT = {
    'Bao lâu nên đổi laptop, điện thoại hay gear? Đừng nâng theo đời máy — hãy nâng khi bottleneck có giá':
        'Bao lâu nên đổi laptop, điện thoại hay gear? Đừng chạy theo đời mới — hãy đổi khi máy thật sự cản trở công việc',
    'Không có chu kỳ 2, 3 hay 5 năm đúng cho mọi thiết bị. Nên đổi khi một bottleneck đo được làm mất thời gian/thu nhập, khi độ tin cậy gây downtime, khi pin/repair không còn kinh tế hoặc phần mềm quan trọng hết hỗ trợ. Nếu máy hiện tại vẫn hoàn thành workload trong thời gian chấp nhận được, nâng chỉ vì đời mới thường đem lại ROI thấp hơn tối ưu workflow hoặc giữ tiền cho lần nâng cấp lớn hơn.':
        'Không có mốc 2, 3 hay 5 năm nào đúng cho mọi thiết bị. Chỉ nên đổi khi máy hiện tại bắt đầu làm chậm công việc, hay lỗi khiến mình mất thời gian, pin xuống cấp quá nặng, chi phí sửa chữa không còn hợp lý hoặc phần mềm quan trọng không còn được hỗ trợ. Nếu máy vẫn đáp ứng tốt nhu cầu hằng ngày, đổi chỉ vì có đời mới thường không đáng bằng việc tối ưu cách làm việc hoặc để dành tiền cho một lần nâng cấp thật sự cần thiết.',
}

# Một số cụm sau khi dịch máy móc vẫn chưa tự nhiên, xử lý thêm lần nữa.
CLEANUPS = [
    ('một điểm nghẽn đo được', 'một vấn đề rõ ràng'),
    ('làm mất thời gian/thu nhập', 'làm mình mất thời gian hoặc tiền bạc'),
    ('pin/repair không còn kinh tế', 'pin xuống cấp hoặc chi phí sửa chữa không còn hợp lý'),
    ('hoàn thành khối lượng công việc trong thời gian chấp nhận được', 'vẫn xử lý công việc hằng ngày trong thời gian mình thấy ổn'),
    ('mức độ đáng tiền thấp hơn tối ưu quy trình làm việc', 'kém đáng tiền hơn việc tối ưu cách làm việc'),
    ('quy trình làm việc creator', 'quy trình làm việc của người làm nội dung'),
    ('quy trình làm việc AI', 'công việc có dùng AI'),
    ('thông tin hãng công bố marketing', 'thông tin quảng cáo do hãng công bố'),
]

BANNED = [
    r'\bbottleneck\b', r'\bworkload\b', r'\bdowntime\b', r'\bworkflow\b',
    r'\bROI\b', r'\btrade[- ]?off\b', r'\bvendor claim\b', r'\blab claim\b',
    r'\bscaling\b', r'\brefresh rate\b', r'\bcolor profile\b', r'\bpolling rate\b',
    r'\bform factor\b', r'\bthroughput\b', r'\bspec sheet\b', r'\buse case\b',
    r'\bfuture[- ]?proof', r'\bthermal budget\b', r'\bdaily driver\b',
]

SKIP_PREFIXES = (
    'slug:', 'image:', 'tags:', 'url:', 'source_url:', 'source_name:',
)


def transform_line(line: str, in_sources: bool, in_code: bool) -> str:
    stripped = line.strip()
    if in_code or in_sources or stripped.startswith(SKIP_PREFIXES):
        return line
    if 'http://' in line or 'https://' in line:
        return line

    out = line
    for old, new in EXACT.items():
        out = out.replace(old, new)
    for pattern, replacement in REPLACEMENTS:
        out = re.sub(pattern, replacement, out, flags=re.IGNORECASE)
    for old, new in CLEANUPS:
        out = out.replace(old, new)
    return out


def process(path: Path):
    original = path.read_text(encoding='utf-8')
    lines = original.splitlines(keepends=True)
    out = []
    in_sources = False
    in_code = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            out.append(line)
            continue
        if stripped == 'sources:':
            in_sources = True
            out.append(line)
            continue
        # sources kết thúc ở các field top-level quen thuộc sau block nguồn.
        if in_sources and line and not line.startswith((' ', '\t')) and stripped and stripped != 'sources:':
            in_sources = False
        out.append(transform_line(line, in_sources, in_code))

    updated = ''.join(out)
    if updated != original:
        path.write_text(updated, encoding='utf-8')
        return True
    return False


def visible_text_for_check(path: Path) -> str:
    lines = path.read_text(encoding='utf-8').splitlines()
    out = []
    in_sources = False
    in_code = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if stripped == 'sources:':
            in_sources = True
            continue
        if in_sources and line and not line.startswith((' ', '\t')) and stripped and stripped != 'sources:':
            in_sources = False
        if in_code or in_sources or stripped.startswith(SKIP_PREFIXES):
            continue
        if 'http://' in line or 'https://' in line:
            continue
        out.append(line)
    return '\n'.join(out)


changed = []
for path in sorted(ROOT.glob('*.md')):
    # Áp dụng cho toàn bộ thư viện hiện có để Batch 1–4 không sót bài khó đọc,
    # đồng thời an toàn với các batch mới vì chỉ thay jargon nằm trong danh sách.
    if process(path):
        changed.append(str(path))

problems = []
for path in sorted(ROOT.glob('*.md')):
    text = visible_text_for_check(path)
    for pattern in BANNED:
        if re.search(pattern, text, flags=re.IGNORECASE):
            problems.append(f'{path}: {pattern}')

print(f'Naturalized {len(changed)} posts')
for item in changed:
    print('  -', item)

if problems:
    print('\nCác từ khó hiểu vẫn còn trong phần người đọc nhìn thấy:')
    for item in problems:
        print('  -', item)
    raise SystemExit(1)
